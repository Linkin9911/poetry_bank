# src/utils.py
import json
import os
from typing import Dict
from typing import List


def read_json_file(file_path: str) -> List[Dict]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями или пустой список в случае ошибки.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except json.JSONDecodeError, IOError:
        return []
