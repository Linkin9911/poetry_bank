# src/external_api.py
import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.exchangeratesapi.io/v1/latest"


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict): Словарь с данными транзакции.

    Returns:
        float: Сумма в рублях.
    """
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return float(amount)

    if currency not in ["USD", "EUR"]:
        raise ValueError(f"Unsupported currency: {currency}")

    try:
        response = requests.get(BASE_URL, params={"access_key": API_KEY, "base": currency, "symbols": "RUB"})
        response.raise_for_status()
        rates = response.json().get("rates", {})
        rub_rate = rates.get("RUB", 1.0)
        return float(amount * rub_rate)
    except requests.RequestException:
        raise ConnectionError("Failed to fetch exchange rates")
