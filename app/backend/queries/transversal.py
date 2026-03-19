from app.backend.database import mongo

def query27():
    """
    Renvoie les films qui ont des genres en commun mais qui ont des réalisateurs différents
    """
    pipeline = [
        {"$project": {"title": 1, "Director": 1, "genre": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genre"},
        {"$project": {"title": 1, "Director": 1, "genre": {"$trim": {"input": "$genre"}}}},
        {"$group": {"_id": "$genre", "films": {"$push": {"title": "$title", "director": "$Director"}}}},
        {"$match": {"films.1": {"$exists": True}}},
        {"$project": {
            "genre": "$_id",
            "films": {
                "$filter": {
                    "input": "$films",
                    "as": "f",
                    "cond": True
                }
            }
        }}
    ]
    return list(mongo.db.films.aggregate(pipeline))

def query28(driver, actor_name):
    """
    Renvoie les recommandations des films aux utilisateurs en fonction des préférences d'un acteur donné
    """
    query = """
    MATCH (a:Actors {actor: $name})-[:A_JOUER]->(f:films)
    RETURN collect(f.title) AS titles
    """
    with driver.session() as session:
        result = session.run(query, name=actor_name)
        record = result.single()
        played_titles = record["titles"] if record else []

    pipeline = [
        {"$match": {"title": {"$in": played_titles}}},
        {"$project": {"genre": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genre"},
        {"$project": {"genre": {"$trim": {"input": "$genre"}}}},
        {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 3},
        {"$lookup": {
            "from": "films",
            "let": {"g": "$_id"},
            "pipeline": [
                {"$match": {"$expr": {"$regexMatch": {"input": "$genre", "regex": "$$g"}}}},
                {"$match": {"title": {"$nin": played_titles}}},
                {"$limit": 5}
            ],
            "as": "recommendations"
        }}
    ]
    return list(mongo.db.films.aggregate(pipeline))

def query29(driver):
    """
    Créer une relation de concurrance entre réalisateurs ayant réalisé des films similaires dans la même année
    """
    query = """
    MATCH (r1:Realisateur), (r2:Realisateur)
    WHERE r1 <> r2
    MATCH (f1:films {director: r1.director}), (f2:films {director: r2.director})
    WHERE f1.year = f2.year AND f1 <> f2
    MERGE (r1)-[:CONCURRENCE {annee: f1.year}]->(r2)
    """
    with driver.session() as session:
        session.run(query)

def query30(driver):
    """
    Identifie les collaborations fréquentes entre réalisateurs et acteurs
    Analyse si ces collaborations sont un succès ou non
    """
    query = """
    MATCH (a:Actors)-[:A_JOUER]->(f:films)
    WHERE f.revenue IS NOT NULL AND f.votes IS NOT NULL AND toString(f.revenue) <> '' AND toString(f.votes) <> ''
    WITH a, f.director AS realisateur, count(f) AS nb_movies,
        avg(f.revenue) AS avg_revenue, avg(f.votes) AS avg_votes,
        collect(f.title) AS titles
    WHERE nb_movies > 1
    RETURN a.actor AS actor, realisateur, nb_movies, round(avg_revenue*100)/100 AS avg_revenue, round(avg_votes) AS avg_votes, titles
    ORDER BY nb_movies DESC, avg_revenue DESC
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        return [{"actor": record["actor"], 
                 "realisateur": record["realisateur"], 
                 "nb_movies": record["nb_movies"], 
                 "avg_revenue": record["avg_revenue"], 
                 "avg_votes": record["avg_votes"], 
                 "titles": record["titles"]} for record in result]