# Orchestrateur de Flux de Données avec Apache Airflow

Dans le cadre de mon apprentissage du Data Engineering, j'ai mis en œuvre un orchestrateur de flux de données à l'aide d'Apache Airflow afin d'automatiser des pipelines ETL avec Python et SQLite. Ce travail se concentre sur la planification de tâches (Scheduling), la gestion des dépendances entre opérateurs et la conteneurisation pour comprendre comment les composants (Scheduler, Webserver, Workers) interagissent et réagissent en cas de défaillance.

## Prérequis

- **Docker Desktop** : Installé et lancé (allouer au moins 4 Go de RAM).
- **Terminal** : Git Bash CLI (utilisé dans ce projet), PowerShell ou terminal VS Code.
- **Gestionnaire de paquets** : Utilisation de uv pour l'environnement local.

## Installation & Configuration

1. **Préparer le dossier du projet**

    ```bash
    # Créer et entrer dans le dossier
    mkdir airflow-docker && cd airflow-docker

    # Créer la structure des dossiers pour Docker
    mkdir -p ./dags ./logs ./plugins ./config

    # Initialiser l'environnement Python avec uv
    uv init
    uv add apache-airflow
    ```

2. **Télécharger le Docker Compose officiel**

    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.7/docker-compose.yaml'
    ```

3. **Configuration des permissions et accès**

    L'identifiant AIRFLOW_UID est indispensable pour éviter les erreurs de droits d'écriture sur Windows.

    ```bash
    # OBLIGATOIRE : Fixer l'ID utilisateur
    echo "AIRFLOW_UID=50000" > .env

    # OPTIONNEL : Si vous voulez des identifiants personnalisés (sinon : airflow/airflow)
    # echo "_AIRFLOW_WWW_USER_USERNAME=votre_nom" >> .env
    # echo "_AIRFLOW_WWW_USER_PASSWORD=votre_password" >> .env
    ```

4. **Initialisation et Lancement**

    ```bash
    # Initialiser la base de données (Attendre le message "Exit 0")
    docker compose up airflow-init

    # Lancer les services en arrière-plan
    docker compose up -d
    ```

## Gestion des Utilisateurs

Créer un nouvel admin manuellement :  
Si Airflow est déjà lancé, vous pouvez ajouter un utilisateur via cette commande :

```bash
docker compose run airflow-worker airflow users create \
     --username mon_admin \
     --firstname Jean \
     --lastname Dupont \
     --role Admin \
     --email admin@example.com \
     --password mon_password
```

## Accès à l'Interface

Une fois les conteneurs "Healthy" dans Docker Desktop :

- URL : [http://localhost:8080](http://localhost:8080)
- Utilisateur par défaut : airflow
- Mot de passe par défaut : airflow

## Maintenance et Nettoyage

Pour réinitialiser complètement le projet et supprimer toutes les données (volumes, base de données, conteneurs) :

```bash
# Arrêter et supprimer volumes + orphelins
docker compose down --volumes --remove-orphans

# Nettoyer les fichiers locaux (logs et plugins)
rm -rf ./logs/* ./plugins/*
```

## Structure du Projet

- `/dags` : Scripts Python de vos pipelines (ETL).
- `/logs` : Journaux d'exécution des tâches.
- `docker-compose.yaml` : Fichier de configuration de l'infrastructure.
- `pyproject.toml` : Dépendances Python gérées par uv.
  