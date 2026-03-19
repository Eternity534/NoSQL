from flask import Flask, jsonify
from app.backend.database import init_db, load_mongo_data, load_neo4j_data
from os import environ
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


def create_app():
    app = Flask(__name__)
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../app/.env"))
    SECRET = environ.get("SECRETKEY", "ez")
    assert SECRET != "", "SECRET_KEY not set"
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE="Lax",
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SAMESITE="Lax",
        PREFERRED_URL_SCHEME="https",
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )

    mongo = init_db(app)
    load_mongo_data()
    driver = load_neo4j_data()
    from app.routes import bp

    # Enregistrement automatique dans l'application flask des routes dans le fichier routes.py
    app.register_blueprint(bp)
    return app
