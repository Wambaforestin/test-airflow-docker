from airflow.sdk import dag, task

@dag(
    dag_id="first_parallel_dag",
)
def first_parallel_dag():
    @task.python
    def first():
        print("The first dag")
        return "output1"
    
    @task.python
    def second():
        print("The seconde dag")
        return "output2"
    
    @task.python
    def third(var1, var2):
        print(f"{var1} and {var2}")
    
    parallel_task1 = first()
    parallel_task2 = second()
    
    third(parallel_task1, parallel_task2)
    
first_parallel_dag()