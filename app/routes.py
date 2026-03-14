from flask import Blueprint, jsonify, render_template
from app.backend.queries import *

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    films = query1()
    return render_template("index.html", films=films)
