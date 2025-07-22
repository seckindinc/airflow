from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    "owner": "seckindinc",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="taskflow_api_dag",
    default_args=default_args,
    description="TaskFlow API example DAG",
    start_date=datetime(2024, 1, 1),
    max_active_runs=1,
)
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {"name": "Seckin", "last_name": "Dinc"}

    @task
    def get_age():
        return 30

    @task
    def hello_world(name, last_name, age):
        print("Hello, World!")
        print(f"My name is {name} {last_name} and I am {age} years old.")

    name_dict = get_name()  # This task returns a dictionary with name and last_name
    age = get_age()
    hello_world(name_dict["name"], name_dict["last_name"], age)


dag_instance = hello_world_etl()
