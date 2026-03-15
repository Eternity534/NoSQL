from flask import Blueprint, jsonify, render_template, Response
from app.backend.queries import *
from app.backend.stats import movies_years_histogramm

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    films = query1()
    return render_template("index.html", films=films)


# API routes :
@bp.route("/histogram/movies-per-years")
def movies_per_years():

    data = query4()
    img = movies_years_histogramm(data)

    return Response(img.getvalue(), mimetype="image/png")
