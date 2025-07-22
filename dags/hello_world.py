from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": timedelta(days=1),
}


def hello_world(ti, age):
    name = ti.xcom_pull(
        task_ids="get_name"
    )  # Pull the name from the XCom of the previous task
    if not name:
        name = "Default Name"  # Fallback if no name is provided
    if not age:
        age = 25
    if not isinstance(age, int):
        raise ValueError("Age must be an integer.")
    if age < 0:
        raise ValueError("Age cannot be negative.")
    # Print the message
    print(f"Task ID: {ti.task_id}")
    print(f"Execution Date: {ti.execution_date}")

    print("Hello, World!")
    print(f"My name is {name} and I am {age} years old.")


def get_name():
    return "Seckin"


with DAG(
    dag_id="hello_world_dag_v4",
    default_args=default_args,
    description='A simple DAG that prints "Hello, World!"',
    start_date=datetime(2024, 1, 1),
    max_active_runs=1,
    catchup=False,
    tags=["example"],
) as dag:
    task_1 = PythonOperator(
        task_id="hello_world_task",
        python_callable=hello_world,
        op_kwargs={"age": 30},  # Example parameters for the callable
    )

    task_2 = PythonOperator(task_id="get_name", python_callable=get_name)

    # task_3 = PythonOperator(
    #    task_id="final_task",
    #    python_callable=lambda: print("This is the final task in the DAG."),
    # )
    # task_1 >> [
    #    task_2,
    #    task_3,
    # ]  # Task dependency: task_1 must complete before task_2 and task_3 run

    task_2 >> task_1  # Task dependency: task_2 must complete before task_1 runs
