from typing import final
import pymongo
import streamlit as st
from pymongo import MongoClient
import json


@st.cache_resource
def init_mongo_connection():
    """
    Fonction initialisant la connexion avec la BDD mongo.
    Initialisation de la db `entertainment` et `films`

    """
    # .streamlit/secrets.toml in app/
    mongo = pymongo.MongoClient(**st.secrets["mongo"])
    db = mongo["entertainment"]
    collection = db["films"]
    return mongo, collection


def load_data(collection, json_path="../data/movies.json"):
    """
    Ajout des données de la base par défaut.
    Cinéma
    """
    if collection.count_documents({}) > 0:
        return
    data = []
    with open(json_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    collection.insert_many(data)


"""
def connectionDB():
    mongoUri = os.getenv("MONGO_URI")
    neo4jUri = "neo4j+s://0f675ee5cdb0dea7179c259604399722.bolt.neo4jsandbox.com:443"  # os.getenv("NEO4J_URI") pb connexion à régler
    neo4jAuth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_MDP"))

    mongo_client = MongoClient(
        mongoUri,
        server_api=ServerApi(version="1", strict=True, deprecation_errors=True),
    )

    neo4j_client = GraphDatabase.driver(neo4jUri, auth=neo4jAuth)

    return mongo_client, neo4j_client


if __name__ == "__main__":
    try:
        mongo, neo4j = connectionDB()

        # test mongo
        mongo.admin.command("ping")
        print("Connexion réussi à MongoDB")

        # test neo4j
        neo4j.verify_connectivity()
        print("Connexion réussi à Neo4j")

    except Exception as e:
        print(f"erreur de connexion : {e}")
    finally:
        mongo.close()
        neo4j.close()
"""
