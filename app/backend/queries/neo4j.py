from app.backend.database import mongo

def query14(driver):
    """
    Renvoie l'acteur ayant joué dans le plus grand nombre de films
    """
    query = """
    MATCH (a:Actors)-[:A_JOUER]->(f:films)
    RETURN a.actor AS actor_name, count(f) AS movie_count
    ORDER BY movie_count DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        return {"name": record["actor_name"], "count": record["movie_count"]}

def query15(driver):
    """
    Renvoie les acteurs ayant joué dans des films avec l'actrice Anne Hathaway
    """
    query = """
    MATCH (anne:Actors {actor: 'Anne Hathaway'})-[:A_JOUER]->(f:films)<-[:A_JOUER]-(a:Actors)
    WHERE a.actor <> 'Anne Hathaway'
    RETURN DISTINCT a.actor AS actor_name
    """
    with driver.session() as session:
        result = session.run(query)
        return [record["actor_name"] for record in result]

def query16(driver):
    """
    Renvoie l'acteur ayant joué dans des films totalisant le plus de revenus
    """
    query = """
    MATCH (a:Actors)-[:A_JOUER]->(f:films)
    RETURN a.actor AS actor_name, max(f.revenue) AS maxRevenue
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        return {"name": record["actor_name"], "revenue": record["maxRevenue"]}

def query17(driver):
    """
    Renvoie la moyenne des votes
    """
    query = """
    MATCH (f:films)
    RETURN avg(f.votes) AS avg_votes
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        return {"avg_votes": record["avg_votes"]}

def query18():
    """
    Renvoie le genre le plus représenté dans la db
    """
    pipeline = [
        {"$project": {"genre": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genre"},
        {"$project": {"genre": {"$trim": {"input": "$genre"}}}},
        {"$group": {"_id": "$genre", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 1}
    ]
    return list(mongo.db.films.aggregate(pipeline))

def query19(driver, name):
    """
    Renvoie les films dans lesquels les acteurs ayant joué avec nous ont également joué
    """
    query = """
    MATCH (me:Actors {actor: $name})-[:A_JOUER]->(f1:films)<-[:A_JOUER]-(a:Actors)
    MATCH (a)-[:A_JOUER]->(f2:films)
    WHERE f2 <> f1 AND a.actor <> $name
    RETURN DISTINCT f2.title AS movieTitle
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        return [record["movieTitle"] for record in result]

def query20(driver):
    """
    Renvoie le réalisateur ayant travaillé avec le plus d'acteurs distincts
    """
    query = """
    MATCH (r:Realisateur)
    MATCH (f:films {director: r.director})<-[:A_JOUER]-(a:Actors)
    RETURN r.director AS realisateur, count(DISTINCT a) AS nbActors
    ORDER BY nbActors DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        return {"name": record["realisateur"], "count": record["nbActors"]}

def query21(driver):
    """
    Renvoie les films les plus connectés (ayant le plus d'acteurs en commun)
    """
    query = """
    MATCH (f1:films)<-[:A_JOUER]-(a:Actors)-[:A_JOUER]->(f2:films)
    WHERE f1._id < f2._id
    RETURN f1.title AS film1, f2.title AS film2, count(a) AS commonActors
    ORDER BY commonActors DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return [f"{rec['film1']} and {rec['film2']} share {rec['commonActors']} actors" for rec in result]

def query22(driver):
    """
    Renvoie les 5 acteurs ayant joué avec le plus de réalisateurs différents
    """
    query = """
    MATCH (a:Actors)-[:A_JOUER]->(f:films)
    RETURN a.actor AS Actor, count(DISTINCT f.director) AS nbDirector
    ORDER BY nbDirector DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return [{"actor": record["Actor"], "count": record["nbDirector"]} for record in result]

def query23():
    """
    Renvoie le film le plus recommandé pour un acteur en fonction des genres où il a déjà joué
    """
    pipeline = [
    {"$match": {"Actors": {"$regex": "Anne Hathaway", "$options": "i"}}},
    {"$project": {"genre": {"$split": ["$genre", ","]}}},
    {"$unwind": "$genre"},
    {"$project": {"genre": {"$trim": {"input": "$genre"}}}},
    {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
    ]
    return list(mongo.db.films.aggregate(pipeline))

def query24(driver):
    """
    Créer la relation INFLUENCE_PAR
    """
    query = """
    MATCH (r1:Realisateur), (r2:Realisateur)
    WHERE r1 <> r2
    MATCH (f1:films {director: r1.director})<-[:A_JOUER]-(a:Actors)-[:A_JOUER]->(f2:films {director: r2.director})
    MERGE (r1)-[:INFLUENCE_PAR {raison: "Acteurs communs"}]->(r2)
    """
    with driver.session() as session:
        session.run(query)

def query25(driver, name1, name2):
    """
    Renvoie le chemin le plus court entre deux acteurs donnés
    """
    query = """
    MATCH (p1:Actors {actor: $act1}), (p2:Actors {actor: $act2})
    MATCH p = shortestPath((p1)-[:A_JOUER*..10]-(p2))
    RETURN p
    """
    with driver.session() as session:
        result = session.run(query, act1=name1, act2=name2)
        record = result.single()
        if not record:
            return "Aucun chemin trouvé."
        path = record["p"]
        nodes = [node["actor"] if "Actors" in node.labels else node["title"] 
                 for node in path.nodes]
        return " -> ".join(nodes)
    
def query26(driver):
    """
    Renvoie les groupes d'acteurs qui ont tendance à travailler ensemble
    """
    query = """
    MATCH (a1:Actors)-[:A_JOUER]->(f:films)<-[:A_JOUER]-(a2:Actors)
    WHERE a1.actor < a2.actor
    WITH a1, a2, count(f) AS nb_collaborations, collect(f.title) AS films_communs
    WHERE nb_collaborations > 1
    RETURN a1.actor AS acteur1, a2.actor AS acteur2, nb_collaborations, films_communs
    ORDER BY nb_collaborations DESC
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]