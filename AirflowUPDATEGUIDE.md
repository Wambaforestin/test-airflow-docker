# Nouvelle Syntaxe Airflow : TaskFlow API

Depuis Airflow 2.0, la TaskFlow API permet d'écrire des DAGs de façon plus moderne, lisible et Pythonique. Les fonctions Python deviennent des tâches grâce au décorateur @task, et la gestion des dépendances se fait naturellement par appel de fonctions.

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
	dag_id="etl_taskflow",
	start_date=datetime(2023, 1, 1),
	schedule="@daily",
)
def etl():

	@task
	def extract():
		return "raw data"

	@task
	def transform(data):
		return data.upper()

	@task
	def load(data):
		print(f"Loaded: {data}")

	load(transform(extract()))

etl()
```
# 🧠 Différences Clés à Connaître

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

✔️ **Avantages de la nouvelle méthode**
- Plus propre, Pythonique et moderne
- Les fonctions deviennent des tâches
- Passage automatique des données (XCom)
- Support des type hints
- Plus facile à tester
- Moins de code répétitif
- DAGs plus lisibles et modulaires

**Différences clés à retenir**

1. Les task_id sont automatiques (le nom de la fonction)
2. Les dépendances sont gérées par appel de fonctions
3. Les XCom sont automatiques (retour de fonction)
4. Plus besoin de PythonOperator
5. Le DAG est une fonction décorée, plus un context manager

**Bonnes pratiques modernes**
- Utilisez @dag et @task
- Passez les données via les paramètres de fonction
- Utilisez les type hints
- Gardez des tâches simples et pures
- Privilégiez TaskFlow pour vos pipelines ETL/ELT

**Résumé comparatif**

| Fonctionnalité         | Ancienne Syntaxe | TaskFlow API |
|------------------------|------------------|--------------|
| Création des tâches    | Operators        | Fonctions décorées |
| XCom                   | Manuel           | Automatique   |
| Dépendances            | >> / <<          | Appels de fonctions |
| Lisibilité             | Moyenne          | Excellente    |
| Boilerplate            | Élevé            | Faible        |
| Recommandé             | ❌ Non           | ✔️ Oui        |

La nouvelle syntaxe est plus propre, plus sûre, plus Pythonique, et c'est la méthode recommandée aujourd'hui par la communauté Airflow.
