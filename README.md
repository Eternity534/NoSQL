# NoSQL Databases - Project

## Architecture du Projet

Notre projet s'articule de la manière suivante :

```bash
.
├── app
│   ├── backend
│   │   ├── queries
│   │   │   ├── mongodb.py
│   │   │   ├── neo4j.py
│   │   │   └── transversal.py
│   │   ├── database.py
│   │   └── queries.py
│   ├── static
│   │   └── css
│   │       └── main.css
│   ├── templates
│   │   ├── index.html
│   │   ├── edit.html
│   │   ├── neo4j.html
│   │   ├── transversal.html
│   │   └── nav.html
│   ├── __init__.py
│   └── routes.py
├── data
│   └── movies.json
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

### Explications du backend

- `database.py`: ce fichier contient les fonctions python permettant la connexion aux bases de données _mongodb_ et _ne4j_.
  - `initdb(app)`: cette fonction gère l'initialisation de la connexion entre la base de données _mongo_ et notre application _flask_.
    Dans le cas où la base de données **entertainment** et la collections **films** sont vide, cette fonction vas appeler la fonction `load_mongo_data()`.
  - `load_mongo_data()`: cette fonction va prendre en entrée le fichier `../data/movies.json` qui contient les données par défaut de notre bases de films.

- `stats.py`: ce fichier contient les 3 fonctions permettant de généré dynamiquement les histogramme et graph demandées en utilisant les librairies **seaborn**, **matplotlib** et **numpy**

**queries/** :

- `mongodb.py`: ce fichier contient les requetes faites à la base de données mongo suivant les données demandées dans l'énoncé du sujet.
- `neo4j.py`: ce fichier propose la meme logique que `mongodb.py` mais pour les requetes à la base de données neo4j.
- `transversal.py`: ce fichier contient toute les requetes transversal faites pour mongodb et neo4j_config

### Explications du front-end

**templates/** :

- `index.html`: ce fichier contient l'affichage des parties avec _mongodb_.
- `neo4j.html`:ce fichier contient également l'affichages des requetes mais cette fois pour _neo4j_
- `transversal.html`: ce fichier contient l'affichage des requetes transverse pour _mongo_ et _neo4j_
- `edit.html`: ce fichier contient les formulaires permettant de modifier, supprimer et ajouter des données dans la base de données _mongo_
- `nav.html`: ce fichier contient le menu de navigation réutilisé comme component.

**static/css**:

- `main.css`: ce fichier gère l'aspect visuelle de notre app.
  - Transaprence sur l'IA : Utilisation de l'IA afin de corriger de nombreuses erreurs dans notre css. Nous considérions que le focus attendu de ce cours était surtout sur le backend et les queries des bases de données.

**data/**:

- `movies.json`: ce fichier contient les données json de la base de donnée initiale.

### Spécificité Flask

- `__init__.py` : Ce fichier gère l'initialisation de l'application flask et les différentes configurations notamment de sécurité de l'app.
- `routes.py`: Ce fichier gère les déclarations des routes de l'applications.
  - Les routes et fonctions déclarant les chemins de l'app : `"/"`,`"/edit"` etc.
  - Les routes API sont également déclarer dans la seconde partie du fichier (exemple: `"/edit/update"`)

## Configuration Docker

- `Dockerfile`: ce fichier définie la génération de l'image docker de notre application.
  - Utilisation d'une version _python3-slim_ et de l'option no-cache afin d'avoir l'image la plus petite possible.
  - Installation des dépendances avec le fichier `requirements.txt`
  - Lancement de l'application avec _gunicorn_
- `docker-compose.yaml`: ce fichier lance tous nos conteneurs

### Configuration des volumes

- mongo_data : `/data/db` (garde en mémoire les modifications de la base de données après la première initialisation)
- neo4j_data : `/data/` (garde en mémoire les modifications de la db après destruction du docker )
- neo4j_config: `/conf/` (permet d'accelerer le lancement de l'image )

## Gestions des secrets

Les secrets de connexion aux différentes bases de données conteneurisé on été mise dans un fichier `.env`.
Afin de facilité le deploiement de cette application voici un exemple de gestion de secret utilisé pour l'app(fichier `.env.prod`) :

```.md
MONGO_URI=mongodb://localhost:27017/entertainment
MONGO_USER=root
MONGO_PASSWORD=root
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=entertainment
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=rootroot
```

## Documentations utilisée

- [Flask](https://flask-fr.readthedocs.io/)
- [Flask Blueprint](https://flask.palletsprojects.com/en/stable/tutorial/blog/)
- [Flask Py-mongo](https://flask-pymongo.readthedocs.io/en/latest/)
- [Neo4j documentations](https://neo4j.com/docs/)
- [Neo4j docker volumes documentation](https://neo4j.com/docs/operations-manual/current/docker/mounting-volumes/)
- [Mongo documentations](https://www.mongodb.com/docs/manual/)
