# src/external_api.py
from typing import Dict
from typing import Union

import requests


def convert_to_rubles(transaction: Dict[str, Union[str, float]]) -> float:
    amount = transaction["amount"]
    currency = transaction["currency"]

    # Проверка типа перед вызовом upper()
    if isinstance(currency, str):
        if currency.upper() == "RUB":
            return float(amount)
    elif isinstance(currency, float):
        # Если валюта передана как число — это ошибка
        raise ValueError(f"Некорректный тип валюты: {type(currency)}. Ожидается str.")
    else:
        raise ValueError(f"Неподдерживаемый тип валюты: {type(currency)}")

    # Параметры для API-запроса
    params = {
        "access_key": "LTUWdwz0RWzRoWVFERtduwV2pX2RqMXy",
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }

    url = "https://api.apilayer.com/exchangerates_data/convert"

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            converted_amount = data.get("result")
            if converted_amount is not None:
                return float(converted_amount)
            else:
                raise ValueError('Поле "result" отсутствует в ответе API')
        else:
            error_msg = f"API вернул статус {response.status_code}: {response.text}"
            raise requests.exceptions.RequestException(error_msg)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        raise
