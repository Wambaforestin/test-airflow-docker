from airflow.sdk import dag, task

default_args = {
    'owner': 'airflow',
    # 'retries': 1
}

@dag(
    dag_id='parallel_processing_dag',
    default_args=default_args,
    # schedule_interval='@daily',
    # catchup=False,
    # start_date=datetime(2024, 6, 1),
    # tags=['parallel', 'example']
)
def parallel_processing_dag():
    @task.python
    def extract_from_sources():
        # Extract fake dicts and JSON from multiple sources
        print("Extracting data from API and files...")
        api_data = {
            "source": "API",
            "data": [
                {"id": 1, "value": "A"},
                {"id": 2, "value": "B"}
            ]
        }
        return api_data

    @task.python
    def load_to_s3(api_data):
        # saving the extracted data as json
        import json
        with open('data.json', 'w') as f:
            json.dump(api_data, f)
        # Load extracted data to S3
        print("Loading data to S3...")
        # Simulate S3 path return
        return {'s3_path': 's3://bucket/data.json'}

    @task.python
    def load_to_db(api_data):
        # flatten the data and load to database
        flattened_data = api_data['data']
        # Load extracted data to database
        print("Loading data to database...")
        return {'db_records': len(flattened_data)}

    @task.python
    def transform_data(s3_info, db_info):
        # Transform and clean data
        print("Transforming data...")
        # simulate transformation result
        transformed_data = {
            "s3_path": s3_info['s3_path'],
            "db_records": db_info['db_records'],
            "status": "transformed"
        }
        return transformed_data

    # Define dependencies
    extracted_data = extract_from_sources()
    s3_result = load_to_s3(extracted_data)
    db_result = load_to_db(extracted_data)
    transform_data(s3_result, db_result)

parallel_processing_dag()
