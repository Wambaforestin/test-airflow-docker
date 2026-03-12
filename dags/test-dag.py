from airflow.sdk import dag, task

@dag(
    dag_id="first_dag",
)
def first_dag():
    @task.python
    def first_task():
        print("This is the first task.")
        return "done1"

    @task.python
    def second_task(prev):
        print("This is the second task.")
        return "done2"

    @task.python
    def third_task(prev):
        print("This is the third and last task. Yes, finally!")

    # Strict sequential execution: first -> second -> third
    a = first_task()
    b = second_task(a)
    third_task(b)

first_dag()