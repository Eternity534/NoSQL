from flask import Blueprint, jsonify, render_template, Response
from app.backend.queries.mongodb import *
from app.backend.stats import movies_years_histogramm

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template(
        "index.html", q1=query1(), q2=query2(), q3=query3(), q5=query5(), q6=query6()
    )


# API routes :
@bp.route("/histogram/movies-per-years")
def movies_per_years():

    data = query4()
    img = movies_years_histogramm(data)

    return Response(img.getvalue(), mimetype="image/png")
