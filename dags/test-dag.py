from airflow.sdk import dag, task

@dag(
    dag_id="first_dag",
)
def first_dag():
    
    @task.python
    def first_task():
        print("This is the first task.")
        
    @task.python
    def second_task(var):
        print("This is the secode task.")
        
    @task.python
    def third_task(var):
        print("The is the third and last task. Yes, finally!")
        
    # defining dependencies
    third_task(second_task(first_dag()))
    
first_dag()