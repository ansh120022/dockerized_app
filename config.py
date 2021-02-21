"""Конфигурация приложения."""


class Config(object):
    """Конфигурация приложения."""

    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:postgres@localhost/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Это для прода, когда он будет."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Это для дев-среды."""

    DEVELOPMENT = True
    DEBUG = True
