from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='first_parallel_dag',
    default_args=default_args,
    tags=['parallel', 'xcom']
) as dag:

    def first(**context):
        print("The first dag")
        context['ti'].xcom_push(key='output1', value='output1')

    def second(**context):
        print("The seconde dag")
        context['ti'].xcom_push(key='output2', value='output2')

    def third(**context):
        var1 = context['ti'].xcom_pull(task_ids='first', key='output1')
        var2 = context['ti'].xcom_pull(task_ids='second', key='output2')
        print(f"{var1} and {var2}")

    first_task = PythonOperator(
        task_id='first',
        python_callable=first,
        dag=dag,
    )

    second_task = PythonOperator(
        task_id='second',
        python_callable=second,
        dag=dag,
    )

    third_task = PythonOperator(
        task_id='third',
        python_callable=third,
        dag=dag,
    )

    [first_task, second_task] >> third_task