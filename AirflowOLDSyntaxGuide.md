# Ancienne Syntaxe Airflow (pré‑2.0)

Avant Airflow 2.0, la création des tâches se faisait manuellement avec des opérateurs, l'attribution d'IDs, et la gestion des dépendances avec >> ou <<. Voici un exemple :

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extracting...")

def transform():
    print("Transforming...")

def load():
    print("Loading...")

with DAG(
    dag_id="etl_old_style",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load
    )

    extract_task >> transform_task >> load_task
```
# Différences Clés à Connaître

1. **Les task_id sont automatiques**
     - Ancien :
         ```python
         PythonOperator(task_id="extract", ...)
         ```
     - Airflow attribue automatiquement le task_id avec le nom de la fonction dans la nouvelle API.

2. **Les dépendances sont des appels de fonctions Python**
     - Ancien :
         ```python
         extract_task >> transform_task
         ```
     - Nouveau :
         ```python
         transform(extract())
         ```
     - Cela rend le DAG plus lisible et vraiment Pythonique.

3. **Les XComs sont automatiques**
     - Ancien :
         ```python
         return value  # mais il fallait le récupérer manuellement
         ```
     - Nouveau :
         ```python
         @task
         def extract():
                 return "hello"
         ```
     - Airflow passe automatiquement la valeur de retour à la tâche suivante.

4. **Plus besoin de PythonOperator**
     - Ancien :
         ```python
         PythonOperator(...)
         ```
     - Nouveau :
         ```python
         @task
         def my_task():
                 ...
         ```
     - Plus simple, plus propre, plus Pythonique.

5. **Le DAG est une fonction décorée, plus un context manager**
     - Ancien :
         ```python
         with DAG(...) as dag:
                 ...
         ```
     - Nouveau :
         ```python
         @dag(...)
         def my_dag():
                 ...
         ```

**Problèmes de l'ancienne méthode**

- Beaucoup de code répétitif (boilerplate)
- Plus difficile à tester
- Passage de données entre tâches complexe
- Verbeux et moins Pythonique
- Risque d'erreurs sur les task_id
- Pas de type hints
- Gestion manuelle des XCom

**À éviter aujourd'hui**

- Ne créez plus manuellement de PythonOperator
- N'utilisez plus with DAG: sauf cas particulier
- N'écrivez pas vos DAGs comme des scripts, mais comme des modules Python
- N'utilisez pas la gestion manuelle des XCom

> Passez à la TaskFlow API pour des DAGs plus propres, testables et modernes !
