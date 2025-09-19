
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import xarray as xr
from pathlib import Path
import json
import urllib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

from geopy.distance import geodesic
from meteostat import Point, Daily

from torch_geometric_temporal.signal.static_graph_temporal_signal import StaticGraphTemporalSignal
from torch_geometric_temporal.signal.dynamic_graph_temporal_signal import DynamicGraphTemporalSignal
from torch_geometric_temporal.signal import temporal_signal_split
import torch
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import A3TGCN


##################
# Read Data
##################

fp = r'/Users/koraykinik/PycharmProjects/ercot/ercot_dataset.csv'

df = pd.read_csv(fp).drop(['Unnamed: 0'], axis=1).sort_values(by=['Delivery Date', 'Settlement Point']).reset_index(drop=True)
df[['lat', 'lon']] = df['coords'].str.replace('(', '').str.replace(')', '').str.split(', ', expand=True).astype(float)

point_dict = {'LZ_AEN':0, 'LZ_CPS':1, 'LZ_HOUSTON':2, 'LZ_LCRA':3, 'LZ_NORTH':4, 'LZ_RAYBN':5, 'LZ_SOUTH':6}
df['point'] = df['Settlement Point'].map(point_dict)
df = df.drop(['coords', 'Settlement Point'], axis=1)
df.columns = df.columns.str.lower().str.replace(' ', '', regex=True)
df['deliverydate'] = pd.to_datetime(df['deliverydate'])

##################
# Scale
##################

cols = 'settlementpointprice surfacetemp load gasprice oilprice coalprice windspeed'.split()
df_scaled = df.copy()
df_scaled.loc[:, cols] = StandardScaler().fit_transform(df[cols])
df_scaled.head()

# static edge indexes
distance_matrix = df_scaled.drop_duplicates(subset=['point'], keep='first')[['point', 'lat', 'lon']]
distance_matrix = distance_matrix.merge(distance_matrix, how='cross').reset_index(drop=True)
distance_matrix['distance'] = distance_matrix.apply(lambda x: geodesic((x['lat_x'], x['lon_x']), (x['lat_y'], x['lon_y'])).meters, axis=1)
distance_matrix = distance_matrix.sort_values(by='point_x').reset_index(drop=True)
edge_index = distance_matrix[['point_x', 'point_y']].values.transpose()


distance_feature = distance_matrix["distance"].values
edge_type_feature = np.zeros_like(distance_feature) # 0 = static edge
flow_feature = np.zeros_like(distance_feature) # 0 = no information
static_edge_features = np.stack([distance_feature, edge_type_feature, flow_feature]).transpose()

# build dataset

def extract_dynamic_edges():

    # distance_feature & edge_index -> subset f(x)

    edge_type_feature = np.ones_like(distance_feature)
    flow_feature = np.random.normal(0, 1, len(distance_feature))
    edge_features = np.stack([distance_feature, edge_type_feature, flow_feature]).transpose()

    return edge_features, edge_index


start_date = df_scaled['deliverydate'].min()
end_date = df_scaled['deliverydate'].max()
interval = timedelta(days=1)

cols = 'settlementpointprice surfacetemp load gasprice oilprice coalprice windspeed'.split()
array = df_scaled[cols].values.reshape(-1, 7, 7)

xs = []
edge_indices = []
ys = []
y_indices = []
edge_features = []

days = df_scaled['deliverydate'].unique()
sequence_len = 21
prediction_len = 1

for i in range(len(days) - int(sequence_len + prediction_len - 1)):

    prev_days = array[i:i+sequence_len,:,:]
    curr_day = array[i+sequence_len:i+sequence_len+prediction_len,:,:]

    node_feats = prev_days
    y = curr_day[:,:,0]

    edge_feats, additional_edge_index = extract_dynamic_edges()
    exteneded_edge_index = np.concatenate([edge_index, additional_edge_index], axis=1)
    extended_edge_feats = np.concatenate([edge_feats, static_edge_features], axis=0)

    xs.append(node_feats) # dynamic
    edge_indices.append(exteneded_edge_index) # static + dynamic
    edge_features.append(extended_edge_feats) # static + dynamic
    ys.append(y) # dynamic


dataset = DynamicGraphTemporalSignal(edge_indices=edge_indices, edge_weights=edge_features, features=xs, targets=ys)
train_dataset, test_dataset = temporal_signal_split(dataset, train_ratio=0.8)
print(train_dataset.snapshot_count, test_dataset.snapshot_count)
# next(iter(train_dataset))

class TemporalGNN(torch.nn.Module):
    def __init__(self, node_features, periods):
        super(TemporalGNN, self).__init__()
        # Attention Temporal Graph Convolutional Cell
        self.tgnn = A3TGCN(in_channels=node_features,
                           out_channels=32,
                           periods=periods)
        # Equals single-shot prediction
        self.linear = torch.nn.Linear(32, periods)

    def forward(self, x, edge_index):
        """
        x = Node features for T time steps
        edge_index = Graph edge indices
        """
        h = self.tgnn(x, edge_index)
        h = F.relu(h)
        h = self.linear(h)
        return h

# train model

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(device.type)

model = TemporalGNN(node_features=7, periods=1).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
model.train()

train_losses = []
print("Running training...")
for epoch in range(500):
    print(f'epoch {epoch}')
    loss = 0
    step = 0
    for snapshot in train_dataset:
        snapshot = snapshot.to(device)
        y_hat = model(snapshot.x, snapshot.edge_index)
        loss += torch.mean((y_hat-snapshot.y)**2)
        step += 1

    loss = loss / (step + 1)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    train_losses += [loss.item()]

plt.plot(train_losses)
plt.xlabel('epochs')
plt.ylabel('MSE')
plt.grid()
plt.title('train loss')
plt.show()

# evaluation

model.eval()
loss = 0
step = 0

predictions = []
labels = []

test_losses = []

for snapshot in test_dataset:
    snapshot = snapshot.to(device)

    y_hat = model(snapshot.x, snapshot.edge_index)
    loss += torch.mean((y_hat-snapshot.y)**2)
    test_losses += [loss.item()]

    labels.append(snapshot.y)
    predictions.append(y_hat)

print('eval shapes', predictions[0].shape, labels[0].shape, len(predictions), len(labels))

# y_hats vs actual labels of test data
preds = np.array([p.detach().cpu().numpy() for p in predictions])
labs = np.array([l.cpu() for l in labels])
labs = labs.reshape(-1,7)

# unscale
std = df['settlementpointprice'].std()
mean = df['settlementpointprice'].mean()

# plot
labs_df = pd.DataFrame(labs * std + mean)
preds_df = pd.DataFrame(preds[:,:,0] * std + mean)

# plot
plt.figure(figsize=(20,5))

for s in range(7):
    sns.lineplot(data=labs_df[s], label=f"true, station={s}", color='b', alpha=(s+1)/7)
    sns.lineplot(data=preds_df[s], label=f"pred, station={s}", color='r', alpha=(s+1)/7)

plt.grid()
plt.title('test data')
plt.xlabel('days')
plt.ylabel('MSE')
plt.show()