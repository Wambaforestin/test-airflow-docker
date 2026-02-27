# Airflow Docker - Data Engineering Project

Dans le cadre de mon apprentissage du `Data Engineering`, j'ai voulu tester et mettre en œuvre un orchestrateur de flux de données à l'aide d'Apache Airflow afin d'automatiser des pipelines ETL avec Python et SQLite. Ce travail se concentre sur la planification de tâches (Scheduling), la gestion des dépendances entre opérateurs et la conteneurisation pour comprendre comment les différents composants (Scheduler, Webserver, Workers) interagissent.

## Prérequis

- **Docker Desktop** : Installé et lancé.
- **Ressources** : Allouer au moins 4 Go de RAM dans les paramètres Docker.
- **Terminal** : PowerShell ou terminal VS Code.
- **Gestionnaire de paquets** : Utilisation de `uv` pour l'environnement local.

## Installation

### 1. Préparer l'environnement

```powershell
# Créer le dossier du projet
mkdir airflow-docker
cd airflow-docker

# Créer la structure des dossiers
mkdir -p ./dags ./logs ./plugins ./config

# Initialiser l'environnement Python avec uv
uv init
uv add apache-airflow
```

### 2. Récupérer Docker Compose

```powershell
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.7/docker-compose.yaml'
```

### 3. Configuration & Initialisation

```powershell
# Définir l'ID utilisateur pour les permissions
echo "AIRFLOW_UID=50000" > .env

# Initialiser la base de données et le compte admin
docker compose up airflow-init
```
Attendre le message `Exit 0` confirmant la création de l'admin.

### 4. Lancer Airflow

```powershell
docker compose up -d
```

## Accès à l'interface

Une fois les conteneurs marqués "Healthy" dans Docker Desktop :

- **URL** : [http://localhost:8080](http://localhost:8080)
- **Utilisateur** : airflow
- **Mot de passe** : airflow

## Structure du Projet

- `/dags` : Déposez vos scripts Python Airflow ici.
- `/logs` : Journaux d'exécution des tâches.
- `docker-compose.yaml` : Configuration de l'infrastructure.
- `pyproject.toml` : Géré par uv pour vos dépendances Python locales.