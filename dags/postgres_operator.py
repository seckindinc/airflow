from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="postgres_operator_dag",
    default_args=default_args,
    description="A DAG that uses SQLExecuteQueryOperator to execute PostgreSQL commands",
    start_date=datetime(2025, 7, 10),  # Start date for the DAG
    max_active_runs=1,
    schedule="@daily",  # Daily schedule
    catchup=False,  # Disable catchup to avoid backfilling
)
def postgres_operator_dag():
    task_1 = SQLExecuteQueryOperator(
        task_id="create_postgres_table",
        conn_id="postgres",  # Connection ID (note: parameter name changed from postgres_conn_id)
        sql="""
            CREATE TABLE IF NOT EXISTS public.example_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT
            );
        """,
    )

    task_3 = SQLExecuteQueryOperator(
        task_id="select_from_postgres_table",
        conn_id="postgres",
        sql="""
            SELECT * FROM public.example_table;
        """,
    )

    task_1 >> task_3  # Set task dependencies


dag_instance = postgres_operator_dag()
