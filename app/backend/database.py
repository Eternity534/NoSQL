from flask_pymongo import PyMongo
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


def load_data(json_path="../data/movies.json"):
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
