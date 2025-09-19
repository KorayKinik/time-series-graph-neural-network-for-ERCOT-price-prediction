import boto3
from pathlib import Path

if __name__ == '__main__':

    s3folder = 's3://myercotdata/ercot_data/processed/np_dataset'  # TODO change this bs!
    bucket = boto3.Session().resource('s3').Bucket('myercotdata')
    objects = bucket.objects.filter(Prefix=s3folder)
    existing_files = [obj.key.split("/")[-1] for obj in objects if obj.key.endswith('npz')]

    folder = Path(r'/Users/koraykinik/Library/CloudStorage/GoogleDrive-koraykinik1984@gmail.com/My Drive/np_dataset')
    files = Path(folder).rglob('*.npz')
    files = sorted(files, key=lambda x: int(Path(x).stem.split('arr_')[1]))

    for i, f in enumerate(files):
        fn = f'{s3folder}/{f.name}'
        if Path(fn).name in existing_files:
            print(f"file {i + 1} of {len(files)} \texists skip")
        else:
            print(f"file {i + 1} of {len(files)} \tuploading {str(f)} -> {fn}")
            bucket.upload_file(str(f), fn)
