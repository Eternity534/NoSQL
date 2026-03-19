from flask import Blueprint, jsonify, render_template, Response
from app.backend.queries.mongodb import *
from app.backend.stats import (
    movies_years_histogramm,
    runtime_vs_revenue_scatter,
    avg_runtime_per_decade_histogramm,
)
from app.backend.queries.neo4j import *
from app.backend.queries.transversal import *
from app import driver

bp = Blueprint("main", __name__)

#Nom des membres du projet
MEMBER_ACTOR_1 = "Louis Minotte"
MEMBER_ACTOR_2 = "Paul Ballagny"

#Acteur exemple
ACTOR_1 = "Ben Affleck"
ACTOR_2 = "Chris Pratt"

@bp.route("/")
def index():
    return render_template(
        "index.html",
        q1=query1(),
        q2=query2(),
        q3=query3(),
        q5=query5(),
        q6=query6(),
        q7=query7(),
        q8=query8(),
        q9=query9(),
        q10=query10(),
        q11=query11(),
    )

@bp.route("/neo4j")
def neo4j():
    query24(driver)
    return render_template(
        "neo4j.html",
        q14=query14(driver),
        q15=query15(driver),
        q16=query16(driver),
        q17=query17(driver),
        q18=query18(),
        q19=query19(driver, MEMBER_ACTOR_1),
        q19v2=query19(driver, MEMBER_ACTOR_2),
        q20=query20(driver),
        q21=query21(driver),
        q22=query22(driver),
        q23=query23(),
        q25=query25(driver, ACTOR_1, ACTOR_2),
        q26=query26(driver),
    )

@bp.route("/transversal")
def transversal():
    query29(driver)
    return render_template(
        "transversal.html",
        q27=query27(),
        q28=query28(driver, "Anne Hathaway"),
        q30=query30(driver),
    )

@bp.route("/edit")
def edit():
    all_films = list(mongo.db.films.find({}, {"_id": 0, "title": 1, "year": 1}))
    return render_template("edit.html", all_films=all_films)


# API routes :
@bp.route("/histogram/movies-per-years")
def movies_per_years():

    data = query4()
    img = movies_years_histogramm(data)

    return Response(img.getvalue(), mimetype="image/png")


@bp.route("/histogram/runtime-vs-revenue")
def runtime_vs_revenue():
    data = query12()
    img = runtime_vs_revenue_scatter(data)
    return Response(img.getvalue(), mimetype="image/png")


@bp.route("/histogram/avg-runtime-per-decade")
def avg_runtime_per_decade():
    data = query13()
    img = avg_runtime_per_decade_histogramm(data)
    return Response(img.getvalue(), mimetype="image/png")


## API pour l'édition des données dans la base mongodb
