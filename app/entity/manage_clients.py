"""Функции для работы с моделью клиентов."""
from typing import Any
from sqlalchemy.orm import sessionmaker
from .models import Clients
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/postgres")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def client_data(values: dict) -> Clients:
    """Чтение параметров из запроса."""
    to_insert = Clients(name=values["name"], is_vip=values["is_vip"])
    return to_insert


def insert_client(data: Clients) -> None:
    """Занести в базу клиента."""
    client = session.query(Clients).filter_by(name=data.name).first()
    if client:
        session.delete(client)
    session.add(data)
    session.commit()
    session.close()


def find_client(Clients_id: int) -> Any:
    """Найти клиента по ID."""
    try:
        client = session.query(Clients).filter_by(id=Clients_id).first()
        res = {"id": client.id, "name": client.name, "is_vip": client.is_vip}
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Объект в базе не найден"


def delete_client(Clients_id: int) -> Any:
    """Удалить клиента из базы."""
    try:
        client = session.query(Clients).filter_by(id=Clients_id).first()
        res = {"id": client.id, "name": client.name, "is_vip": client.is_vip}
        session.delete(client)
        session.commit()
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Объект в базе не найден"
