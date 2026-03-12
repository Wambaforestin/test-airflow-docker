from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
import random
import json

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='parallel_processing_dag_with_branching',
    default_args=default_args,
    tags=['parallel', 'branching']
) as dag:

    # tasks

    def extract_from_sources(**context):
        print("Extracting data from API and files...")
        data = {
            "source": "API",
            "data": [
                {"id": 1, "value": "A"},
                {"id": 2, "value": "B"}
            ]
        }
        # Push the extracted data to XCom for downstream tasks
        context['ti'].xcom_push(key='extract_output', value=data)


    def load_to_s3(**context):
        api_data = context['ti'].xcom_pull(task_ids='extract_from_sources', key='extract_output')
        with open('data.json', 'w') as f:
            json.dump(api_data, f)
        print("Loading data to S3...")
        context['ti'].xcom_push(key='s3_output', value={'s3_path': 's3://bucket/data.json'})


    def load_to_db(**context):
        api_data = context['ti'].xcom_pull(task_ids='extract_from_sources', key='extract_output')
        flattened_data = api_data['data']
        print("Loading data to database...")
        context['ti'].xcom_push(key='db_output', value={'db_records': len(flattened_data)})


    def transform_data(**context):
        ti = context['ti']
        s3_output = ti.xcom_pull(task_ids='load_to_s3', key='s3_output')
        db_output = ti.xcom_pull(task_ids='load_to_db', key='db_output')
        print("Transforming data...")
        ti.xcom_push(key='transformed_output', value={
            "s3_path": s3_output['s3_path'],
            "db_records": db_output['db_records'],
            "status": "transformed"
        })


    def decider(**context):
        transformed_output = context['ti'].xcom_pull(task_ids='transform_data', key='transformed_output')
        print("Checking data quality...")
        if transformed_output['db_records'] > 1:
            print("Data quality is good.")
        else:
            print("Data quality is poor.")
        return 'load_final' if random.choice([True, False]) else 'no_load'


    def load_final(**context):
        transformed_output = context['ti'].xcom_pull(task_ids='transform_data', key='transformed_output')
        print(f"Loaded {transformed_output['db_records']} records")
        print("Final load executed...")


    def no_load(**context):
        print("There is a problem with the data...")
        print("Load skipped")


    # operators
    extract_task = PythonOperator(
        task_id='extract_from_sources',
        python_callable=extract_from_sources,
        dag=dag,
    )

    load_s3_task = PythonOperator(
        task_id='load_to_s3',
        python_callable=load_to_s3,
        dag=dag,
    )

    load_db_task = PythonOperator(
        task_id='load_to_db',
        python_callable=load_to_db,
        dag=dag,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        dag=dag,
    )

    branch_task = BranchPythonOperator(
        task_id='decider',
        python_callable=decider,
        dag=dag,
    )

    load_final_task = PythonOperator(
        task_id='load_final',
        python_callable=load_final,
        dag=dag,
    )

    no_load_task = PythonOperator(
        task_id='no_load',
        python_callable=no_load,
        dag=dag,
    )

    # dependencies 

    extract_task >> [load_s3_task, load_db_task] >> transform_task >> branch_task >> [load_final_task, no_load_task]