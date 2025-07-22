from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": timedelta(days=1),
}


def hello_world(ti):
    name = ti.xcom_pull(
        task_ids="get_name", key="name"
    )  # Pull the name from the XCom of the previous task
    last_name = ti.xcom_pull(
        task_ids="get_name", key="last_name"
    )  # Pull the last name from the XCom of the previous task
    age = ti.xcom_pull(
        task_ids="get_age", key="age"
    )  # Pull the age from the XCom of the previous task

    print("Hello, World!")
    print(f"My name is {name}, my surname is {last_name} and I am {age} years old.")


def get_name(ti):
    ti.xcom_push(key="name", value="Seckin")
    ti.xcom_push(key="last_name", value="Dinc")


def get_age(ti):
    ti.xcom_push(key="age", value=30)


with DAG(
    dag_id="multiple_xcoms_dag",
    default_args=default_args,
    description="Multiple Xcom examples DAG",
    start_date=datetime(2024, 1, 1),
    max_active_runs=1,
    catchup=False,
    tags=["example"],
) as dag:
    task_1 = PythonOperator(
        task_id="hello_world_task",
        python_callable=hello_world,
    )

    task_2 = PythonOperator(task_id="get_name", python_callable=get_name)
    task_3 = PythonOperator(task_id="get_age", python_callable=get_age)

    (
        task_2 >> task_3 >> task_1
    )  # Task dependency: task_2 and task_3 must complete before task_1 runs
