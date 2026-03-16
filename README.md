# NoSQL Databases - Project

## Architecture du Projet

Le projet s'organise de la façon suivante :

```
.
├── app
│   ├── backend
│   │   ├── database.py
│   │   └── queries.py
│   ├── static
│   ├── templates
│   │   └── index.html
│   ├── __init__.py
│   └── routes.py
├── data
│   └── movies.json
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Initialisation du projet

```bash
# Initialisation de l'environement virtuel
python -m venv .venv
# Pour Linux :
source ./venv/bin/activate
# Pour windows :
.venv\Scripts\activate.bat


# Installation des dépendances :
pip install -r requirements.txt
```

## Docker configurations :

#### Neo4j

Volumes :

- mongo_data : `/data/db` (garde en mémoire les modifications de la base de données après la première initialisation)
- neo4j_data : `/data/` (garde en mémoire les modifications de la db après destruction du docker )
- neo4j_config: `/conf/` (permet d'accelerer le lancement de l'image )

## TODO :

CREER UN FORMULAIRE POUR ajouter supprimer et modifier les données d'un films
