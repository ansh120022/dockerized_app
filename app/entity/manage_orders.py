"""Функции для работы с моделю заказов."""
from typing import Any
from sqlalchemy.orm import sessionmaker
from .models import Orders, Drivers
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/postgres")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def order_data(values: dict) -> Orders:
    """Создание объекта класса Orders с полученным параметрами."""
    new_order = Orders(
        address_from=values["address_from"],
        address_to=values["address_to"],
        client_id=values["client_id"],
        driver_id=values["driver_id"],
        date_created=datetime.now(),
        status=values["status"],
    )
    return new_order


def insert_order(data: Orders) -> None:
    """Коммит в БД."""
    session.add(data)
    session.commit()
    session.close()


def find_order(order_id: str) -> Any:
    """Поиск заказа в бд по id."""
    try:
        order = session.query(Orders).filter_by(id=order_id).first()
        res = {
            "client_id": order.client_id,
            "driver_id": order.driver_id,
            "date_created": order.date_created,
            "status": order.status,
            "address_from": order.address_from,
            "address_to": order.address_to,
        }
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Объект в базе не найден"


def get_order_status(order_id: int) -> Any:
    """Узнать статус заказа по id."""
    try:
        order = session.query(Orders).filter_by(id=order_id).first()
        res = {"status": order.status}
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Объект в базе не найден"


def update_status(order_id: int, status: str) -> Any:
    """Апдейт статуса заказа."""
    if status in ["not_accepted", "in_progress", "done", "cancelled"]:
        try:
            order = session.query(Orders).filter_by(id=order_id).first()
            res = {
                "id": order.id,
                "address_from": order.address_from,
                "address_to": order.address_to,
                "client_id": order.client_id,
                "driver_id": order.driver_id,
                "date_created": order.date_created,
                "status": status,
            }
            data = order_data(res)
            session.query(Orders).filter_by(id=order_id).update(
                {Orders.status: data.status}
            )
            session.commit()
            session.close()
            return res
        except AttributeError:
            session.close()
            return "Объект в базе не найден"
    else:
        session.close()
        return "Некорретный запрос"


def update_order(order_id: int, data) -> Any:
    """Обновление данных заказа."""
    try:
        order = session.query(Orders).filter_by(id=order_id).first()
        if order.status == "not_accepted":
            session.query(Orders).filter_by(id=order_id).update(
                {
                    Orders.id: order_id,
                    Orders.client_id: data.client_id,
                    Orders.address_from: data.address_from,
                    Orders.address_to: data.address_to,
                    Orders.status: data.status,
                }
            )
        else:
            session.query(Orders).filter_by(id=order_id).update(
                {
                    Orders.address_from: data.address_from,
                    Orders.address_to: data.address_to,
                    Orders.status: data.status,
                }
            )
        res = {
            "id": order.id,
            "address_from": order.address_from,
            "address_to": order.address_to,
            "client_id": order.client_id,
            "driver_id": order.driver_id,
            "date_created": order.date_created,
            "status": order.status,
        }
        session.commit()
        session.close()
        return res
    except AttributeError:
        session.close()
        return "Ошибка в запросе"


