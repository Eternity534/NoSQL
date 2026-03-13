#contient la connexion aux deux databases
import os
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from neo4j import GraphDatabase

def connectionDB():
    mongoUri = os.getenv("MONGO_URI")
    neo4jUri = "neo4j+s://0f675ee5cdb0dea7179c259604399722.bolt.neo4jsandbox.com:443" #os.getenv("NEO4J_URI") pb connexion à régler
    neo4jAuth = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_MDP"))

    mongo_client = MongoClient(mongoUri, server_api=ServerApi(
        version="1", strict=True, deprecation_errors=True
    ))

    neo4j_client = GraphDatabase.driver(neo4jUri, auth=neo4jAuth)

    return mongo_client, neo4j_client

if __name__ == "__main__":
    try:
        mongo, neo4j = connectionDB()

        #test mongo
        mongo.admin.command('ping')
        print("Connexion réussi à MongoDB")

        #test neo4j
        neo4j.verify_connectivity()
        print("Connexion réussi à Neo4j")

    except Exception as e:
        print(f"erreur de connexion : {e}")
    finally:
        mongo.close()
        neo4j.close()