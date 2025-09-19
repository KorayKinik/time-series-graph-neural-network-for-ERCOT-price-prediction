from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

python_exec = r'/Users/koraykinik/miniconda3/envs/ercot/bin/python'
python_file = r'/Users/koraykinik/PycharmProjects/ercot/src/scrapers/download_data_parallel.py'


dataset = 'solar_power_production'
LAST_PAGE = 420
CHUNKS = 30

tuples = [(min(range(LAST_PAGE+1)[i:i+CHUNKS]), max(range(LAST_PAGE+1)[i:i+CHUNKS])) for i in range(1, len(range(LAST_PAGE+1)), CHUNKS)]

for i, j in tuples:

    text = f'{dataset}_pages_{str(i).zfill(4)}_to_{str(j).zfill(4)}'

    with DAG(text,
             start_date=datetime(2024, 11, 20),
             schedule=None,
             catchup=False,
             concurrency=10,
             max_active_runs=5,
             ) as dag:

        task = BashOperator(
            task_id=text,
            depends_on_past=False,
            bash_command=f'{python_exec} {python_file} --dataset {dataset} --start_page {i} --end_page {j}',
            retries=3,
            retry_delay=timedelta(minutes=1),
            wait_for_downstream=False,
            dag=dag
        )
