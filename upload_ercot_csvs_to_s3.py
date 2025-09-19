

import os
import time
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
import zipfile
from io import StringIO, BytesIO
import boto3

BUCKET = 'myercotdata'
URL = 'https://www.ercot.com/mp/data-products/data-product-details?id='
URLS_HISTORICAL = {
    'dam_shadow_prices':                URL + 'NP4-191-CD',  # 1/1/2022 is page 22
    'dam_hourly_lmps':                  URL + 'NP4-183-CD',  # 1/1/2022 is page 22
    'rtm_lmps_by_electrical_bus':       URL + 'NP6-787-CD',  # 1/1/2022 is page 6178. say 6400
    'rtm_sced_shadow_prices':           URL + 'NP6-86-CD',   # 1/1/2022 is page 480. say 500
    'seven_day_load_forecast':          URL + 'NP3-565-CD',  # 1/1/2022 is page 508. say 530
    'solar_power_production':           URL + 'NP4-745-CD',  # 1/1/2022 is page 421. say 450
    'wind_power_production':            URL + 'NP4-742-CD',  # 1/1/2022 is page 507. say 530
    'actual_system_load':               URL + 'NP6-345-CD',  # 1/1/2022 is page 22
    'hourly_resource_outage':           URL + 'NP3-233-CD',  # 1/1/2022 is page 508. say 530
}
S3FOLDER_HISTORICAL = r'ercot_data/historical'


if __name__ == '__main__':

    for dataset in sorted(URLS_HISTORICAL.keys()):

        print(f"\n{'*' * 20}\ndataset {dataset}\n{'*' * 20}")

        s3folder = f"{S3FOLDER_HISTORICAL}/{dataset}"
        bucket = boto3.Session().resource('s3').Bucket(BUCKET)
        objects = bucket.objects.filter(Prefix=s3folder)
        existing_files = [obj.key.split("/")[-1] for obj in objects if obj.key.endswith(('csv', 'xlsx'))]
        LOCAL = Path(r'/Users/koraykinik/Library/CloudStorage/GoogleDrive-koraykinik1984@gmail.com/My Drive/ERCOT data')
        source = LOCAL / dataset
        files = sorted(source.rglob("*.csv"))
        cutoff = datetime.strptime('2022_01_01', '%Y_%m_%d')

        print(f"S3 existing_files length: {len(existing_files)}")
        print(f"local files length: {len(files)}")

        for i, f in enumerate(files):
            ts = f.name.split('_csv_')[-1].split('.csv')[0]
            ts = datetime.strptime(ts, '%Y_%m_%d_%H_%M_%S')
            if ts >= cutoff and f.name not in existing_files:
                fn = f'{s3folder}/{f.name}'
                print(f"file {i+1} of {len(files)} \tuploading {str(f)} -> {fn}")
                bucket.upload_file(str(f), fn)
            else:
                print(f"file {i+1} of {len(files)} \tskipping {str(f)}")




