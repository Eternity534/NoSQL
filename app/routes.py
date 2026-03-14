from flask import Blueprint, jsonify
from app.backend.queries import *

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return f"{query1()}"
