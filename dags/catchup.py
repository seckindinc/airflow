from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="catchup_dag",
    default_args=default_args,
    description="A DAG to demonstrate catchup",
    max_active_runs=1,
    start_date=datetime(2025, 6, 6),  # Start date for the DAG
    schedule="@daily",  # Daily schedule
    catchup=True,  # Enable catchup to backfill missed runs
) as dag:

    task = BashOperator(
        task_id="task_1",
        bash_command="echo This is the first task in the DAG!",
    )
