from airflow.sdk import dag, task

@dag(
    dag_id="xcom_dag",
)
def xcom_dag():
    @task.python
    def push_xcom():
        print("Pushing XCom value...")
        fetch_date = {
            "name": 'Airflow',
            "description": 'XCom example',
            "date": "2024-06-01",
            "status": "success"
        }
        return fetch_date

    @task.python
    def pull_transform_xcom(value: dict):
        print("Pulling XCom value...")
        print(f"Received XCom value: {value}")
        transformed_value = {
            "name": value["name"].upper(),
            "description": value["description"].capitalize(),
            "date": value["date"].replace("-", "/"),
            "status": value["status"].capitalize()
        }
        print(f"Transformed XCom value: {transformed_value}")
        return transformed_value
    
    @task.python
    def final_task(transformed_value: dict):
        print("Final task received transformed value:")
        print(transformed_value)

    xcom_value = push_xcom()
    transformed_value = pull_transform_xcom(xcom_value)
    final_task(transformed_value)

xcom_dag()