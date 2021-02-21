"""Схемы для валидации пользовательского ввода."""

DRIVERS_SCHEMA = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "car": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "car"
  ]
}

CLIENTS_SCHEMA = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "is_vip": {
      "type": "boolean"
    }
  },
  "required": [
    "name",
    "is_vip"
  ]
}


ORDERS_SCHEMA = {
  "type": "object",
  "properties": {
    "client_id": {
      "type": "string"
    },
    "driver_id": {
      "type": "string"
    },
    "date_created": {
      "type": "string"
    },
    "status": {
      "type": "string"
    },
    "address_from": {
      "type": "string"
    },
    "address_to": {
      "type": "string"
    }
  },
  "required": [
    "client_id",
    "driver_id",
    #"date_created", убираю, так как сделала подстановку текущей даты
    "status",
    "address_from",
    "address_to"
  ]
}
