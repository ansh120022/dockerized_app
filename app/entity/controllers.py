"""Роуты и обработка запросов."""

import json

from flask import request, Blueprint, Response, current_app
from ..validate import json_validate
from app.schema import ORDERS_SCHEMA, CLIENTS_SCHEMA, DRIVERS_SCHEMA

from .manage_clients import (
    client_data,
    insert_client,
    find_client,
    delete_client
)
from .manage_drivers import (
    insert_driver,
    driver_data,
    delete_driver,
    find_driver
)
from .manage_orders import (
    order_data,
    find_order,
    insert_order,
    get_order_status,
    update_order
)

module = Blueprint("entity", __name__)


def log_error(*args, **kwargs):
    """Логирование."""
    current_app.logger.error(*args, **kwargs)


@module.route("/api/v1/drivers", methods=["GET", "POST"])
def drivers() -> Response:
    """Работа с водителями."""
    if request.method == "POST":
        data = request.get_json()
        if json_validate(data, DRIVERS_SCHEMA):
            insert_driver(driver_data(data))
            return Response(status=201, response="created!")
        else:
            return Response(status=400, response="Невалидный запрос")


    if request.method == "GET":
        driver_id = request.headers.get("driverID")
        result = find_driver(driver_id)
        if result == "Объект в базе не найден":
            return Response(status=404, response=result)
        else:
            response_dict = dict(result)
            response = json.dumps(response_dict, ensure_ascii=False)
            return Response(status=200, response=response, mimetype="application/json")


@module.route("/api/v1/drivers/<int:driver_id>", methods=["DELETE"])
def del_driver(driver_id) -> Response:
    """Удаление водителя."""
    if request.method == "DELETE":
        result = delete_driver(driver_id)
        if result == "Объект в базе не найден":
            return Response(status=404, response=result)
        else:
            message = "Удалено"
            response_dict = dict(message=message, driver=result)
            response = json.dumps(response_dict, ensure_ascii=False)
            return Response(status=200, response=response, mimetype="application/json")


@module.route("/api/v1/clients", methods=["GET", "POST"])
def clients() -> Response:
    """Обработка запросов для клиента."""
    if request.method == "POST":
        data = request.get_json()
        if json_validate(data, CLIENTS_SCHEMA):
            insert_client(client_data(data))
            return Response(status=201, response="created!")
        else:
            return Response(status=400, response="Невалидный запрос")
    if request.method == "GET":
        client_id = request.headers.get("clientId")
        result = find_client(client_id)
        if result == "Объект в базе не найден":
            return Response(status=404, response=result)
        else:
            response_dict = dict(result)
            response = json.dumps(response_dict, ensure_ascii=False)
            return Response(status=200, response=response, mimetype="application/json")


@module.route("/api/v1/clients/<int:client_id>", methods=["DELETE"])
def del_client(client_id):
    """Клиенты."""
    result = find_client(client_id)
    if result == "Объект в базе не найден":
        response_dict = dict(message=result)
        response = json.dumps(response_dict, ensure_ascii=False)
        return Response(status=404, response=response, mimetype="application/json")
    else:
        result = delete_client(client_id)
        response_dict = dict(message="Удалено", client=result)
        response = json.dumps(response_dict, ensure_ascii=False)
        return Response(status=200, response=response, mimetype="application/json")
    return Response(status=400, response="Ошибка в запросе")


@module.route("/api/v1/orders", methods=["GET", "POST"])
def orders() -> Response:
    """Работа с закакзами."""
    if request.method == "POST":
        data = request.get_json()
        if json_validate(data, ORDERS_SCHEMA):
            insert_order(order_data(data))
            return Response(status=201, response="created!")
        else:
            return Response(status=400, response="Невалидный запрос")

    if request.method == "GET":
        order_id = request.headers.get("orderId")
        result = find_order(order_id)
        if result == "Объект в базе не найден":
            return Response(status=404, response=result)
        else:
            response_dict = dict(result)
            response = json.dumps(response_dict, ensure_ascii=False)
            return Response(status=200, response=response, mimetype="application/json")


@module.route("/api/v1/orders/<int:order_id>", methods=["PUT"])
def update_order_data(order_id):
    """Обновление заказа."""
    response_status = 200
    new_data = order_data(request.get_json())
    if json_validate(new_data, ORDERS_SCHEMA):
        current_status = get_order_status(order_id)
        if current_status == "Объект в базе не найден":
            return Response(status=404, response="Объект в базе не найден")
        if current_status == "not_accepted" and new_data.status not in [
            "not_accepted",
            "in_progress",
            "cancelled",
        ]:
            response_status = 400
        if current_status == "in_progress" and new_data["status"] not in [
            "in_progress",
            "done",
            "cancelled",
        ]:
            response_status = 400
        if current_status == "cancelled" or current_status == "done":
            response_status = 400
        if response_status == 400:
            return Response(status=response_status, response="Ошибка в запросе")
        else:
            res = update_order(order_id, new_data)
            status = 200
            message = "Изменено!"
            response_dict = dict(message=message, order=res)
            response = json.dumps(response_dict, ensure_ascii=False)
            return Response(status=status, response=response, mimetype="application/json")
    else:
        return Response(status=400, response="Невалидный запрос")
