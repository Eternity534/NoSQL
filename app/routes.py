from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    Response,
    url_for,
    flash,
)
from app.backend.queries.mongodb import *
from app.backend.database import neo4j_connect_db
from app.backend.stats import (
    movies_years_histogramm,
    runtime_vs_revenue_scatter,
    avg_runtime_per_decade_histogramm,
)
from app.backend.queries.neo4j import *
from app.backend.queries.transversal import *

bp = Blueprint("main", __name__)

# Nom des membres du projet
MEMBER_ACTOR_1 = "Louis Minotte"
MEMBER_ACTOR_2 = "Paul Ballagny"

# Acteur exemple
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
    driver = neo4j_connect_db()
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
    """
    Cette fonction permet de rendre le html en mettant en entrée les 3 queries transversale
    """
    driver = neo4j_connect_db()
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


# API routes pour l'édition :
@bp.route("/edit/update", methods=["POST"])
def update_films():
    """
    Fonction qui à partir des données du formulaire va éditer la base de données mongo
    """
    title = request.form.get("title")
    field = request.form.get("field")
    value = request.form.get("value")

    numeric_fields = [
        "year",
        "Runtime (Minutes)",
        "Revenue (Millions)",
        "Metascore",
        "Votes",
    ]
    if field in numeric_fields:
        try:
            value = float(value) if "." in value else int(value)
        except ValueError:
            flash("La valeur doit être un nombre pour ce champ.", "error")
            return redirect(url_for("main.edit"))
    result = mongo.db.films.update_one({"title": title}, {"$set": {field: value}})
    if result.matched_count == 0:
        flash(f"Film '{title}' introuvable.", "error")
    else:
        flash(f"'{title}' mis à jour : {field} → {value}", "success")

    return redirect(url_for("main.edit"))


@bp.route("/edit/add", methods=["POST"])
def add_film():
    """
    Fonction naive d'ajout  de films basé sur le postula que les nom de films sont uniques dans notre cas
    On donne la possibilité que tout les champs ne soient pas obligatoire
    """
    title = request.form.get("title")

    # Vérification de l'existance du film basé sur le titre (à améliorer)
    if mongo.db.films.find_one({"title": title}):
        flash(f"Un film nommé'{title}' existe déjà.", "error")
        return redirect(url_for("main.edit"))

    new_film = {
        "title": title,
        "year": int(request.form.get("year")),
        "genre": request.form.get("genre", ""),
        "Director": request.form.get("Director", ""),
        "Actors": request.form.get("Actors", ""),
        "rating": request.form.get("rating", ""),
        "Description": request.form.get("description", ""),
    }

    runtime = request.form.get("runtime")
    revenue = request.form.get("revenue")
    metascore = request.form.get("metascore")
    votes = request.form.get("votes")
    # On vérifie que les champs on été reseigner et on les convertis car sinon le formulaire les revoies comme string et non comme valeur numérique
    if runtime:
        new_film["Runtime (Minutes)"] = int(runtime)
    if revenue:
        new_film["Revenue (Millions)"] = float(revenue)
    if metascore:
        new_film["Metascore"] = int(metascore)
    if votes:
        new_film["Votes"] = int(votes)

    mongo.db.films.insert_one(new_film)
    flash(f"Film '{title}' ajouté avec succès.", "success")
    return redirect(url_for("main.edit"))


@bp.route("/edit/delete", methods=["POST"])
def delete_film():
    """
    Fonction supprimant le film qui est rentrée dans le formulaire du fichier edit
    """
    title = request.form.get("title")
    result = mongo.db.films.delete_one({"title": title})

    if result.deleted_count == 0:
        flash(f"Film '{title}' impossible à supprimer ")
    else:
        flash(f"Film '{title}' supprimé")
    return redirect(url_for("main.edit"))


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
