from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='more_parallel_dag',
    default_args=default_args,
    tags=['parallel', 'example']
) as dag:

    def task_a(**context):
        print("Task A running...")

    def task_b(**context):
        print("Task B running...")

    def task_c(**context):
        print("Task C running...")

    task_a_op = PythonOperator(
        task_id='task_a',
        python_callable=task_a,
        dag=dag,
    )

    task_b_op = PythonOperator(
        task_id='task_b',
        python_callable=task_b,
        dag=dag,
    )

    task_c_op = PythonOperator(
        task_id='task_c',
        python_callable=task_c,
        dag=dag,
    )

    [task_a_op, task_b_op] >> task_c_op
