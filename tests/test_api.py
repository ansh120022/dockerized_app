"""Happy path всех API-запросов."""

import requests

url = "http://0.0.0.0:5000/api/v1"


def test_add_driver():
    """Добавление водителя."""
    body = {"name": "Анатолий Вассерман", "car": "Volkswagen T5 Caravelle"}
    response = requests.post(url + "/drivers", json=body)
    assert response.status_code == 201


def test_get_driver():
    """Просмотр водителя."""
    response = requests.get(url + "/drivers", headers={"DriverId": "1"})
    assert response.status_code == 200


def test_add_client():
    """Добавление клиента."""
    body = {"name": "Passenger", "is_vip": True}
    response = requests.post(url + "/clients", json=body)
    assert response.status_code == 201


def test_get_client():
    """Просмотр клиента."""
    response = requests.get(url + "/clients", headers={"clientId": "1"})
    assert response.status_code == 200


def test_add_order():
    """Добавление заказа."""
    body = {
        "client_id": "1",
        "driver_id": "1",
        "status": "not_accepted",
        "address_from": "str1",
        "address_to": "str2",
    }
    response = requests.post(url + "/orders", json=body)
    assert response.status_code == 201


def test_get_order():
    """Просмотр заказа."""
    response = requests.get(url + "/orders", headers={"orderId": "1"})
    assert response.status_code == 200


def test_delete_driver():
    """Удаление водителя."""
    response = requests.delete(url + "/drivers/1")
    assert response.status_code == 200


def test_delete_client():
    """Удаление водителя."""
    response = requests.delete(url + "/clients/1")
    assert response.status_code == 200
