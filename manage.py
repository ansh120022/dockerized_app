"""Запуск приложения."""

from flask_script import Manager
from app import create_app

app = create_app()
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://postgres:postgres@localhost/postgres"
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
