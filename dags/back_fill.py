from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="backfill_dag",
    default_args=default_args,
    description="A DAG to demonstrate backfill",
    max_active_runs=1,
    start_date=datetime(2025, 6, 6),  # Start date for the DAG
    schedule="@daily",  # Daily schedule
    catchup=False,  # Enable catchup to backfill missed runs
) as dag:

    task = BashOperator(
        task_id="task_1",
        bash_command="echo This is the first task in the DAG!",
    )
# airflow backfill create --from-date 2025-06-06 --to-date 2025-06-08 --dag-id backfill_dag
