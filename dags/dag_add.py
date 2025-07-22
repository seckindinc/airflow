from airflow.decorators import dag, task
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from pendulum import datetime


@dag(
    dag_id="dag_add",
    start_date=datetime(2025, 6, 1),
    schedule="@daily",
    catchup=False,
    tags=["example"],
    render_template_as_native_obj=True,
    doc_md=__doc__,
)
def dag_add():
    """
    DAG that adds two numbers and triggers a multiplication DAG.
    """

    @task
    def add_numbers() -> int:
        """Add two numbers and return the result."""
        a, b = 3, 7
        result = a + b
        print(f"{a} + {b} = {result}")
        return result

    addition = add_numbers()

    trigger = TriggerDagRunOperator(
        task_id="trigger_dag_multiply",
        trigger_dag_id="dag_multiply",
        conf={
            "sum": "{{ ti.xcom_pull(task_ids='add_numbers') }}"
        },  # XCom pull to get the result
        wait_for_completion=True,
        deferrable=True,
        poke_interval=30,  # Better for deferrable tasks
    )

    addition >> trigger


dag_add()
