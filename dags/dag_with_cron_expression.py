from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_cron_expression",
    default_args=default_args,
    description="A DAG with a cron expression schedule",
    max_active_runs=1,
    start_date=datetime(2025, 6, 6),  # Start date for the DAG
    schedule="0 3 * * Tue",  # Cron expression for daily at 3 AM on Tuesdays and Fridays
    catchup=True,  # Disable catchup to avoid backfilling
) as dag:

    task = BashOperator(
        task_id="task_1",
        bash_command="echo This is the first task in the DAG with a cron expression!",
    )
