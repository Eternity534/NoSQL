from app.backend.database import mongo


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
        {"$match": {"year": {"$gt": 1999}}},
        {"$group": {"_id": 0, "movie_count": {"$sum": 1}}},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query3():
    """
    Q3 : Renvoie la moyenne des votes des films sortis en 2007
    """
    pipeline = [
        {"$match": {"year": 2007}},
        {"$group": {"_id": 0, "avg_votes": {"$avg": "$Votes"}}},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query4():
    """
    Q4 : Renvoie le nombre de films sorti par an
    """
    pipeline = [{"$group": {"_id": "$year", "movie_count": {"$sum": 1}}}]
    return list(mongo.db.films.aggregate(pipeline))


def query5():
    """
    Q5 : Renvoie les genres de films étant dans la base de données
    """
    pipeline = [
        {"$project": {"genres": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genres"},
        {"$group": {"_id": {"$trim": {"input": "$genres"}}}},  # supprime les espaces
        {"$sort": {"_id": 1}},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query6():
    """
    Q6 : Renvoie le film qui a généré le plus de revenu
    """
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$exists": True, "$nin": [None, ""]}}},
        {"$project": {"_id": 0, "title": 1, "year": 1, "rev": "$Revenue (Millions)"}},
        {"$sort": {"rev": -1}},
        {"$limit": 1},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query7():
    """
    Q7 : Renvoie les réalisateurs ayant réalisé plus de 5 films
    """
    pipeline = [
        {"$group": {"_id": "$Director", "movie_count": {"$sum": 1}}},
        {"$match": {"movie_count": {"$gt": 5}}},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query8():
    """
    Q8 : Renvoie le genre de film qui rapporte en moyenne le plus de revenus
    """
    pipeline = [
        {"$group": {"_id": "$genre", "avg_revenu": {"$avg": "$Revenue (Millions)"}}},
        {"$sort": {"avg_revenu": -1}},
        {"$limit": 1},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query9():
    """
    Q9 : Renvoie les 3 films les mieux notés pour chaque décennie
    """
    pipeline = [
        {"$match": {"Metascore": {"$exists": True, "$type": "int"}}},
        {"$sort": {"Metascore": -1}},
        {
            "$group": {
                "_id": {"$subtract": ["$year", {"$mod": ["$year", 10]}]},
                "movies_info": {
                    "$push": {
                        "title": "$title",
                        "year": "$year",
                        "rating": "$Metascore",
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "decennie": "$_id",
                "top3_movies": {"$slice": ["$movies_info", 3]},
            }
        },
        {"$sort": {"decennie": 1}},
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query10():
    """
    Q10 : Renvoie le film le plus long par genre
    """
    pipeline = [
        {"$sort": {"Runtime (Minutes)": -1}},
        {
            "$group": {
                "_id": "$genre",
                "title": {"$first": "$title"},
                "runtime": {"$first": "$Runtime (Minutes)"},
            }
        },
    ]
    return list(mongo.db.films.aggregate(pipeline))


def query11():
    """
    Q11 : Renvoie les films ayant une note supérieure à 80 et ayant généré 50 millions de dollars
    """
    return list(
        mongo.db.films.find(
            {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50.00}}
        )
    )


def query12():
    """
    Q12 : Renvoie la durée des films et leur revenu
    Analyse statistique à faire sur un graphique
    """
    return list(
        mongo.db.films.find(
            {
                "Runtime (Minutes)": {"$exists": True, "$type": "number"},
                "Revenue (Millions)": {"$exists": True, "$type": "number"},
            },
            {"_id": 0, "Runtime (Minutes)": 1, "Revenue (Millions)": 1},
        )
    )


def query13():
    """
    Q13 : Renvoie la durée moyenne des films par décennie
    Analyse à effectuer sur un graphique
    """
    pipeline = [
        {
            "$group": {
                "_id": {"$subtract": ["$year", {"$mod": ["$year", 10]}]},
                "avg_time_length": {"$avg": "$Runtime (Minutes)"},
            }
        },
        {"$project": {"_id": 0, "decennie": "$_id", "avg_time_length": 1}},
        {"$sort": {"decennie": 1}},
    ]
    return list(mongo.db.films.aggregate(pipeline))
