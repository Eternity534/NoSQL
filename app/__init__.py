from flask import Flask
from app.backend.database import init_db, load_data
from os import environ
from flask import jsonify

app = Flask(__name__)
SECRET = environ.get("SECRETKEY", "ez")
assert SECRET != "", "SECRET_KEY not set"
"""
app.config.update(
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SECURE=True,
SESSION_COOKIE_SAMESITE="Lax",
REMEMBER_COOKIE_HTTPONLY=True,
REMEMBER_COOKIE_SECURE=True,
REMEMBER_COOKIE_SAMESITE="Lax",
PREFERRED_URL_SCHEME="https",
SECRET_KEY=SECRET,
)
"""
mongo = init_db(app)
load_data()


@app.route("/")
def index():
    films = list(
        mongo.db.films.find({}, {"_id": 0})
    )  # exclude _id (not JSON serializable)
    return jsonify(films)
