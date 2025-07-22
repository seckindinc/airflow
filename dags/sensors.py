from airflow.decorators import dag, task
from datetime import timedelta
from airflow.utils import timezone
import os

FILE_PATH = "/tmp/airflow_sensor_demo.txt"


@dag(
    schedule="@daily",
    start_date=timezone.utcnow() - timedelta(days=1),
    catchup=False,
    tags=["example", "sensor", "airflow3"],
    max_active_runs=1,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
)
def sensor_decorator_demo_dag():

    @task
    def generate_file_task():
        """Simulate creating a file"""
        with open(FILE_PATH, "w") as f:
            f.write("This is a test file.\n")
        print(f"File created at: {FILE_PATH}")
        return FILE_PATH

    @task.sensor(
        poke_interval=30,  # Best Practice: 30 seconds for responsive checking
        timeout=600,  # Best Practice: 10 minutes timeout
        mode="poke",  # Best Practice: Use poke for short intervals
        retries=3,
        retry_delay=timedelta(minutes=1),
    )
    def wait_for_file_task(file_path: str):
        """Sensor that waits for the file to exist"""
        file_exists = os.path.exists(file_path)
        print(f"Checking for file: {file_path} - Exists: {file_exists}")
        return file_exists

    # Assign tasks and set dependency
    file_path = generate_file_task()
    wait_for_file_task(file_path)


dag = sensor_decorator_demo_dag()
