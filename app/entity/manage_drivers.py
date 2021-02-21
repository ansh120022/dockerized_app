"""Функции для работы с моделью водителей."""
from typing import Any
from sqlalchemy.orm import sessionmaker

from .models import Drivers
from sqlalchemy import create_engine


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/postgres")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def driver_data(values: dict) -> Drivers:
    """Получение параметров запроса."""
    to_insert = Drivers(name=values["name"], car=values["car"])
    return to_insert


def insert_driver(data: Drivers) -> None:
    """Создание нового водителя, либо пересоздание существующего."""
    driver = session.query(Drivers).filter_by(name=data.name).first()
    if driver:
        session.delete(driver)
    session.add(data)
    session.commit()
    session.close()


def find_driver(driver_id: str) -> Any:
    """Нахождение водителя в бд по id."""
    try:
        driver = session.query(Drivers).filter_by(id=driver_id).first()
        res = {"id": driver.id, "name": driver.name, "car": driver.car}
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Объект в базе не найден"


def delete_driver(driver_id: int) -> Any:
    """Удаление водителя из бд."""
    try:
        driver = session.query(Drivers).filter_by(id=driver_id).first()
        res = {"id": driver.id, "name": driver.name, "car": driver.car}
        session.delete(driver)
        session.commit()
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Объект в базе не найден"
