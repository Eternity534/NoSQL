# NoSQL Databases - Project

## Architecture du Projet

Le projet s'organise de la façon suivante :
 .
├──  app
│ ├──  backend
│ │ ├──  database.py
│ │ └──  queries.py
│ ├──  static
│ ├──  templates
│ │ └──  index.html
│ ├──  **init**.py
│ └──  routes.py
├──  data
│ └──  movies.json
├──  docker-compose.yml
├── 󰂺 README.md
└──  requirements.txt

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

## Framework streamlit

```bash
# Lancement du script python `streamlit_app.py`
streamlit run
```

## Base de donnée

Les secrets sont géré dans un fichier toml `.streamlit/secrets.toml`
