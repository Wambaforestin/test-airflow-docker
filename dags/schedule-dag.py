from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from pendulum import datetime # The advantage of using pendulum is that it is timezone aware

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='schedule_dag_run',
    default_args=default_args,
    tags=['schedule', 'example'],
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    is_paused_upon_creation=False,
    catchup=True,

) as dag:

    first_task_op = EmptyOperator(
        task_id='first_task',
        dag=dag,
    )

    second_task_op = EmptyOperator(
        task_id='second_task',
        dag=dag,
    )

    third_task_op = EmptyOperator(
        task_id='third_task',
        dag=dag,
    )

    first_task_op >> second_task_op >> third_task_op