#contient toutes les requêtes pour mongodb et neo4js

#Q1 : Affiche l'année où le plus grand nombre de films ont été sortis
def query1(mongo):
    pipeline = [
        {
            "$group": {
                "_id": "$year",
                "movie_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "movie_count": -1
            }
        },
        {
            "$limit": 1
        }
    ]
    return list(mongo.aggregate(pipeline))

"""
#Q2 : Affiche le nombre de films sortis après 1999
pipeline2 = [
    {"$match": {"year": {"$gt": "1999"}}},
    {
        "$group": {
            "_id": None,
            "movie_count": {"$sum": 1}
        }
    }
]

result2 = list(mongo.aggregate(pipeline2))
st.write(f"Q2 : {result2}")

#Q3 : Affiche la moyenne des votes des films sortis en 2007
pipeline3 = [
    {"$match": {"year": "2007"}},
    {
        "$group": {
            "_id": None,
            "avg_votes": {"$avg": 1}
        }
    }
]

result3 = list(mongo.aggregate(pipeline3))
st.write(f"Q3 : {result3}")

#Q4 : Affiche un histogramme du nombres de films par année
"""
