from flask_pymongo import PyMongo
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../app/.env"))
mongo = PyMongo()


def init_db(app):
    """
    Initialisation de la connexion avec mongo
    """
    mongo_user = os.getenv("MONGO_USER")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = os.getenv("MONGO_PORT")
    mongo_db = os.getenv("MONGO_DB")

    app.config["MONGO_URI"] = (
        f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}"
        f"?authSource=admin"
    )
    collection_name = "films"
    if not collection_name:
        mongo.db.create_collection(collection_name)

    mongo.init_app(app)
    return mongo


def load_mongo_data(json_path="../data/movies.json"):
    """
    Ajout des données de la base par défaut.
    Cinéma
    """
    collection = mongo.db.films
    if collection.count_documents({}) > 0:
        return

    data = []
    with open(json_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    if data:
        collection.insert_many(data)


def neo4j_connect_db():
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    return driver


def load_neo4j_data():
    """
    Importe la data de mongoDB
    Créer les noeuds et relations neo4j
    """

    collection_movies = mongo.db.films  # récupération du json de mongo
    movies = []
    for doc in collection_movies.find({}):  # envoie la data dans un array pour neo4j
        doc["_id"] = str(doc["_id"])
        movies.append(doc)

    REQUEST = """
    UNWIND $list_movies AS value
    MERGE (f:films {_id: toString(value._id)}) //créer un noeud films pour chaque doc de la db
    SET f.title = value.title,
        f.year = value.year,
        f.votes = value.Votes,
        f.revenue = value.`Revenue (Millions)`,
        f.rating = value.rating,
        f.director = value.Director
    WITH f, value WHERE value.Director IS NOT NULL //créer un noeud Realisateur pour chaque director de la db
    MERGE (r:Realisateur {director: value.Director})
    WITH f, value WHERE value.Actors IS NOT NULL //créer un noeud Actors pour chaque acteur de la db
    UNWIND split(value.Actors, ",") AS single_actor //isole les acteurs
    WITH f, trim(single_actor) AS name_actor
    MERGE (a:Actors {actor: name_actor})
    MERGE (a)-[:A_JOUER]->(f) //fait la relation acteur -> film
    RETURN count(f) AS films_traites
    """

    REQUEST_TEAM = """
    MERGE (a1:Actors {actor: "Louis Minotte"})
    MERGE (a2:Actors {actor: "Paul Ballagny"})
    WITH a1, a2
    MATCH (f1:films {title: "Rogue One"})
    MATCH (f2:films {title: "Moana"})
    MERGE (a1)-[:A_JOUER]->(f1)
    MERGE (a2)-[:A_JOUER]->(f2)
    RETURN a1.actor, a2.actor
    """
    driver = neo4j_connect_db()
    with driver.session() as session:
        session.run(REQUEST, list_movies=movies)
        session.run(REQUEST_TEAM)

    return driver
