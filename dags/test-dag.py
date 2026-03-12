from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='first_dag',
    default_args=default_args,
    tags=['test', 'empty']
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