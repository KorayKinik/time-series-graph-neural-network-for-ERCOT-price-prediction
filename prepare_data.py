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


root = Path(r'/Users/koraykinik/PycharmProjects/ercot')

#####################################
# settlement point prices
#####################################
# https://www.ercot.com/mp/data-products/data-product-details?id=NP4-180-ER
# input: daily resolution

fp = root / r'Historical DAM Settlement Point Prices (SPPs) for each of the Hubs and Load Zones'
files = list(Path(fp).rglob('*.xlsx'))
print(len(files), 'files')

dfs = []
for f in files:
    print(f)
    sheets = pd.read_excel(f, sheet_name=None, skiprows=0)
    tables = [d for d in list(sheets.values()) if not d.empty]
    dfp = pd.concat(tables, axis=0)
    dfp = dfp[dfp['Settlement Point'].str.contains('LZ')].copy()
    dfp['Delivery Date'] = pd.to_datetime(dfp['Delivery Date']).dt.date
    dfp = dfp.groupby(['Settlement Point', 'Delivery Date'])['Settlement Point Price'].mean().reset_index()
    coords = {
        'LZ_AEN': (30.237487800746983, -97.68392917943001),
        'LZ_CPS':(29.4303266891018, -98.49104441846484),
        'LZ_HOUSTON':(29.923397953675746, -95.3494704123345),
        'LZ_LCRA':(29.890718549428662, -98.27938192368337),
        'LZ_NORTH':(32.7706229414293, -96.81296426144323),
        'LZ_RAYBN':(33.70950160279557, -96.93286612488266),
        'LZ_SOUTH':(27.84329789105108, -97.37704556282911),
        'LZ_WEST':(32.404236698742984, -99.5900092921979),
    }
    dfp['coords'] = dfp['Settlement Point'].map(coords).reset_index(drop=True)
    dfs.append(dfp)

df_prices = pd.concat(dfs, axis=0).reset_index(drop=True)
df_prices = df_prices.sort_values(by=['Delivery Date', 'Settlement Point']).reset_index(drop=True)

#####################################
# surface temperatures
#####################################
# https://pypi.org/project/meteostat/
# input: daily resolution

start = pd.to_datetime(df_prices['Delivery Date']).min()
end = pd.to_datetime(df_prices['Delivery Date']).max()

dfs = []
sett_points = df_prices.groupby(['Settlement Point'])[['coords']].min().reset_index()
for i, (sp, coords) in sett_points.iterrows():

    location = Point(*coords, 70)
    data = Daily(location, start, end)
    data = data.fetch()['tavg'].reset_index()
    data['Settlement Point'] = sp
    dfs.append(data)

df_temps = pd.concat(dfs, axis=0).reset_index(drop=True).rename(columns={'time': 'Delivery Date'})
df_temps['Delivery Date'] = pd.to_datetime(df_temps['Delivery Date']).dt.date
df_temps['Surface Temp'] = df_temps['tavg'] * 1.8 + 32
df_temps = df_temps[['Delivery Date', 'Settlement Point', 'Surface Temp']]
df_temps = df_temps.sort_values(by=['Delivery Date', 'Settlement Point']).reset_index(drop=True)

#####################################
# ercot load data
#####################################
# https://www.ercot.com/gridinfo/load/load_hist
# input: hourly resolution

fp = root / r'Hourly Load Data Archives'
files = list(Path(fp).rglob('*.[xlsx xls]*'))
print(len(files), 'files')

dfs = []
for f in files:
    print(f)
    dfll = pd.read_excel(f)
    dfll = dfll.reset_index(drop=True).rename(columns={"Hour Ending": "Delivery Date",
                                                       "Hour End": "Delivery Date",
                                                       "HourEnding": "Delivery Date",
                                                       "Hour_End": "Delivery Date",})
    _df = dfll['Delivery Date'].astype(str).str.split(expand=True)
    if f.suffix == '.xls':
        pd.to_datetime(_df[0]) + pd.to_timedelta(_df[1])
    else:
        hrs = pd.to_timedelta(_df[1].apply(lambda x: x if len(x) > 5 else x + ':00'))
        dfll['Delivery Date'] = pd.to_datetime(_df[0], format='mixed') + hrs

    dfll['Delivery Date'] = dfll['Delivery Date'].dt.date
    dfll = dfll.groupby("Delivery Date").mean()
    dfll = dfll.drop(columns=["ERCOT", "FWEST", "FAR_WEST"], errors='ignore')

    col_map = {
        "WEST": 'LZ_AEN',
        "EAST": 'LZ_CPS',
        "COAST": 'LZ_HOUSTON',
        "SCENT": 'LZ_LCRA',
        "NORTH": 'LZ_NORTH',
        "NORTH_C": 'LZ_RAYBN',
        "NCENT": 'LZ_RAYBN',
        "SOUTH": 'LZ_SOUTH',
        "SOUTH_C": 'LZ_LCRA',
        "SOUTHERN": 'LZ_SOUTH',
    }
    dfll = dfll.rename(columns=col_map).stack().reset_index()
    dfll.columns = ["Delivery Date", "Settlement Point", "Load"]
    dfs.append(dfll)

df_loads = pd.concat(dfs, axis=0).reset_index(drop=True)
df_loads = df_loads\
    .drop_duplicates(subset=['Delivery Date', 'Settlement Point'])\
    .sort_values(by=['Delivery Date', 'Settlement Point']).reset_index(drop=True)

#####################################
# Oil, Gas, Coal prices daily
#####################################
# https://markets.businessinsider.com/commodities/natural-gas-price
# https://markets.businessinsider.com/commodities/oil-price
# https://markets.businessinsider.com/commodities/coal-price
# input: daily resolution

fp = root / 'Commodity Data' / r'Natural Gas (Henry Hub)_11_06_24-09_30_13.csv'
df_gas = pd.read_csv(fp)
df_gas = df_gas[["Date", "Open"]].rename(columns={"Open": "Gas Price", "Date": "Delivery Date"})
df_gas['Delivery Date'] = pd.to_datetime(df_gas['Delivery Date']).dt.date
df_gas.set_index('Delivery Date', inplace=True)

fp = root / 'Commodity Data' / r'Oil (WTI)_11_06_24-09_03_13.csv'
df_oil = pd.read_csv(fp)
df_oil = df_oil[["Date", "Open"]].rename(columns={"Open": "Oil Price", "Date": "Delivery Date"})
df_oil['Delivery Date'] = pd.to_datetime(df_oil['Delivery Date']).dt.date
df_oil.set_index('Delivery Date', inplace=True)

fp = root / 'Commodity Data' / r'Coal_11_06_24-09_02_13.csv'
df_coal = pd.read_csv(fp)
df_coal = df_coal[["Date", "Open"]].rename(columns={"Open": "Coal Price", "Date": "Delivery Date"})
df_coal['Delivery Date'] = pd.to_datetime(df_coal['Delivery Date']).dt.date
df_coal.set_index('Delivery Date', inplace=True)

df_commodities = pd.concat([df_gas, df_oil, df_coal], axis=1, join='inner').reset_index()
df_commodities = df_commodities.sort_values(by=['Delivery Date']).reset_index(drop=True)

#####################################
# Wind speed data
#####################################
# https://cds-beta.climate.copernicus.eu/datasets/projections-cmip6?tab=download
# input: daily resolution

fp = root / 'cmip6 data' / 'sfcWind_day_UKESM1-0-LL_ssp126_r1i1p1f2_gn_20150101-20241230.nc'
ds = xr.open_dataset(fp)


def get_wind_speed(latlon, day):
    day = str(day)[:10]
    if "31" in day:
        return None
    else:
        try:
            data = ds.sfcWind.sel(lat=latlon[0], lon=latlon[1], method="nearest").sel(time=str(day))
            return data.values[0]
        except KeyError:
            return None


df_winds = df_prices.copy()
df_winds['Wind Speed'] = df_winds[["coords", "Delivery Date"]].apply(lambda x: get_wind_speed(*x), axis=1)
df_winds = df_winds[['Delivery Date', 'Settlement Point', 'Wind Speed']]

df_joined = df_prices.set_index(['Delivery Date', 'Settlement Point'])\
    .join(df_temps.set_index(['Delivery Date', 'Settlement Point']), how='left')\
    .join(df_loads.set_index(['Delivery Date', 'Settlement Point']), how='left')\
    .join(df_commodities.set_index(['Delivery Date']), how='left')\
    .join(df_winds.set_index(['Delivery Date', 'Settlement Point']), how='left')\
    .reset_index()

#####################################
# Cleaning and imputations
#####################################

df_joined = df_joined[df_joined['Settlement Point'] != 'LZ_WEST']
df_joined = df_joined[df_joined['Delivery Date'] >= pd.to_datetime('2015-01-01').date()]

assert df_joined.groupby(['Delivery Date']).count()['Settlement Point'].unique()[0] == 7

# # interpolate few nulls
cols = ["Oil Price", "Gas Price", "Coal Price", "Wind Speed", "Surface Temp", "Load"]
df_joined[cols] = df_joined[cols].interpolate(method='linear', limit_direction='forward', axis=0)
df_joined[cols] = df_joined[cols].interpolate(method='linear', limit_direction='backward', axis=0)
df_joined = df_joined.sort_values(by=['Delivery Date', 'Settlement Point']).reset_index(drop=True)

df_joined.to_csv(root / 'ercot_dataset.csv')
df_joined

