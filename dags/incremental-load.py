from airflow.sdk import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='incremental_load_dag',
    default_args=default_args,
    tags=['incremental', 'example'],
    start_date=datetime(2026, 3, 10),
    schedule='@daily',
    is_paused_upon_creation=False,
    catchup=True,
) as dag:

    incremental_load_task = SQLExecuteQueryOperator(
        task_id='incremental_load_task',
        conn_id='my_database_connection',
        sql="""
            INSERT INTO warehouse.sales
            SELECT *
            FROM raw.sales
            WHERE updated_at >= '{{ data_interval_start }}' -- using jinja template to access the data interval of the DAG run
              AND updated_at <  '{{ data_interval_end }}';  -- this ensures we only load the new or updated records since the last DAG run.
        """,
        dag=dag,
    )
    
    incremental_load_task
