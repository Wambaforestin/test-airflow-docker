from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='xcom_dag',
    default_args=default_args,
    tags=['xcom', 'example']
) as dag:

    def push_xcom(**context):
        print("Pushing XCom value...")
        fetch_date = {
            "name": 'Airflow',
            "description": 'XCom example',
            "date": "2024-06-01",
            "status": "success"
        }
        context['ti'].xcom_push(key='fetch_date', value=fetch_date)

    def pull_transform_xcom(**context):
        value = context['ti'].xcom_pull(task_ids='push_xcom', key='fetch_date')
        print("Pulling XCom value...")
        print(f"Received XCom value: {value}")
        transformed_value = {
            "name": value["name"].upper(),
            "description": value["description"].capitalize(),
            "date": value["date"].replace("-", "/"),
            "status": value["status"].capitalize()
        }
        context['ti'].xcom_push(key='transformed_value', value=transformed_value)
        print(f"Transformed XCom value: {transformed_value}")

    def final_task(**context):
        transformed_value = context['ti'].xcom_pull(task_ids='pull_transform_xcom', key='transformed_value')
        print("Final task received transformed value:")
        print(transformed_value)

    push_xcom_task = PythonOperator(
        task_id='push_xcom',
        python_callable=push_xcom,
        dag=dag,
    )

    pull_transform_xcom_task = PythonOperator(
        task_id='pull_transform_xcom',
        python_callable=pull_transform_xcom,
        dag=dag,
    )

    final_task_task = PythonOperator(
        task_id='final_task',
        python_callable=final_task,
        dag=dag,
    )

    push_xcom_task >> pull_transform_xcom_task >> final_task_task