"""Описание таблиц в БД."""

from app.database import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Drivers(db.Model):
    """Таблица с водителями."""

    __drivers__ = "drivers"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, comment="ID водителя"
    )
    name = db.Column(db.String, nullable=False, comment="Имя водителя")
    car = db.Column(db.String, nullable=False, comment="Машина водителя")
    orders = relationship("Orders", cascade='all', backref="driver")

    def __init__(self, *args, **kwargs):
        """Конструктор."""
        super(Drivers, self).__init__(*args, **kwargs)


class Clients(db.Model):
    """Таблица с клиентами."""

    __clients__ = "clients"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, comment="ID клиента"
    )
    name = db.Column(db.String, nullable=False, comment="Имя клиента")
    is_vip = db.Column(db.Boolean, nullable=False, comment="Флаг VIP-клиента")
    orders = relationship("Orders", cascade='all', backref="client")

    def __init__(self, *args, **kwargs):
        """Конструктор."""
        super(Clients, self).__init__(*args, **kwargs)


class Orders(db.Model):
    """Таблица с заказами."""

    __orders__ = "orders"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, comment="ID заказа"
    )
    address_from = db.Column(db.String, nullable=False, comment="Адрес отправления")
    address_to = db.Column(db.String, nullable=False, comment="Адрес назначения")
    client_id = db.Column(
        db.Integer, ForeignKey("clients.id"), nullable=False, comment="ID клиента"
    )
    driver_id = db.Column(
        db.Integer, ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False, comment="ID водителя"
    )
    client_id = db.Column(
        db.Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False, comment="ID клиента"
    )
    date_created = db.Column(
        db.String,
        nullable=False,
        default=datetime.now(),
        comment="Время создания заказа",
    )
    status = db.Column(db.String, nullable=False, comment="Статус заказа")

    def __init__(self, *args, **kwargs):
        """Конструктор."""
        super(Orders, self).__init__(*args, **kwargs)
