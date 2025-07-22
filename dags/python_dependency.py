from datetime import datetime, timedelta
from airflow import DAG

from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": timedelta(days=1),
}


def get_pandas_version():
    import pandas as pd

    print(pd.__version__)  # Print the version of pandas to verify installation


with DAG(
    dag_id="python_dependency_dag",
    default_args=default_args,
    description="A DAG that installs a Python dependency",
    start_date=datetime(2024, 1, 1),
    max_active_runs=1,
    catchup=False,
) as dag:
    task_1 = PythonOperator(
        task_id="get_pandas_version",
        python_callable=get_pandas_version,
    )

    task_1  # This task will run the get_pandas function to check the pandas installation
