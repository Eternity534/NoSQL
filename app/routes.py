from flask import Blueprint, jsonify, render_template, Response
from app.backend.queries.mongodb import *
from app.backend.stats import (
    movies_years_histogramm,
    runtime_vs_revenue_scatter,
    avg_runtime_per_decade_histogramm,
)

bp = Blueprint("main", __name__)


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
