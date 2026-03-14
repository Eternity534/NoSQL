from app.backend.database import mongo

# contient toutes les requêtes pour mongodb et neo4js


def query1():
    """
    Q1 : Affiche l'année où le plus grand nombre de films ont été sortis
    """
    pipeline = [
        {"$group": {"_id": "$year", "movie_count": {"$sum": 1}}},
        {"$sort": {"movie_count": -1}},
        {"$limit": 1},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query2():
    """
    Q2 : Affiche le nombre de films sortis après 1999
    """
    pipeline = [
        {"$match": {"year": {"$gt": "1999"}}},
        {"$group": {"_id": None, "movie_count": {"$sum": 1}}},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query3():
    """
    Q3 : Affiche la moyenne des votes des films sortis en 2007
    """
    pipeline = [
        {"$match": {"year": "2007"}},
        {"$group": {"_id": None, "avg_votes": {"$avg": 1}}},
    ]
    return list(mongo.aggregate(pipeline))


# Q4 : Affiche un histogramme du nombres de films par année
