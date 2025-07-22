# dag_multiply.py - APPROACH 1: Pure Trigger-based (Recommended)
from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    dag_id="dag_multiply",
    start_date=datetime(2025, 6, 1),
    schedule=None,  # Triggered DAG
    catchup=False,
    tags=["example"],
    doc_md=__doc__,
    max_active_runs=1,  # Prevent concurrent runs
)
def dag_multiply():
    """
    DAG that multiplies a received sum by 2.
    This DAG is triggered by dag_add via TriggerDagRunOperator.
    """

    @task
    def multiply(**kwargs) -> int:
        """
        Multiply the sum received from the triggering DAG by 2.

        Args:
            **kwargs: Context containing dag_run with configuration

        Returns:
            The multiplied result
        """
        dag_run = kwargs.get("dag_run")
        if dag_run is None or dag_run.conf is None:
            raise ValueError("No configuration received from triggering DAG")

        sum_value = dag_run.conf.get("sum")
        if sum_value is None:
            raise ValueError("No 'sum' value found in DAG configuration")

        # Ensure sum_value is an integer
        if isinstance(sum_value, str):
            sum_value = int(sum_value)

        result = sum_value * 2
        print(f"Multiplying {sum_value} * 2 = {result}")
        return result

    multiply()


dag_multiply()
