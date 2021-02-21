"""Создание приложения и таблиц в БД."""

from flask import Flask
from .database import db
from .entity import controllers as entity


def create_app() -> Flask:
    """Создание приложения с параметрами."""
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://postgres:postgres@localhost/postgres"
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    # if app.debug:
    #     try:
    #         from flask_debugtoolbar import DebugToolbarExtension
    #         toolbar = DebugToolbarExtension(app)
    #     except:
    #         pass

    app.register_blueprint(entity.module)

    return app
