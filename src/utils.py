import json
import logging
import os
from typing import Dict
from typing import List

# Логер для utils (если ещё не создан)
logger_utils = logging.getLogger("utils")


def read_json_file(file_path: str) -> List[Dict]:
    """Читает JSON‑файл и возвращает список словарей с данными о транзакциях."""
    logger_utils.info(f"Попытка прочитать файл: {file_path}")

    if not os.path.exists(file_path):
        logger_utils.error(f"Файл не найден: {file_path}")
        return []

    try:
        logger_utils.debug(f"Файл {file_path} открыт для чтения")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger_utils.info(f"Данные успешно загружены из {file_path}, получено {len(data)} записей")
                return data
            else:
                logger_utils.warning(
                    f"Данные из {file_path} не являются списком "
                    f"(тип: {type(data).__name__}), возвращаем пустой результат"
                )
                return []

    except json.JSONDecodeError as e:
        logger_utils.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except IOError as e:
        logger_utils.error(f"Ошибка ввода‑вывода при чтении файла {file_path}: {str(e)}")
        return []


def filter_by_status(data: list, status: str) -> list:
    """Фильтрует транзакции по статусу (с приведением к нижнему регистру)."""
    target_status = status.lower()
    return [transaction for transaction in data if transaction.get("status", "").lower() == target_status]


def sort_by_date(data: list, ascending: bool = True) -> list:
    """Сортирует транзакции по дате."""
    return sorted(data, key=lambda x: x.get("date", ""), reverse=not ascending)


def filter_ruble_transactions(data: list) -> list:
    """Оставляет только рублёвые транзакции."""
    return [transaction for transaction in data if "руб" in str(transaction.get("currency", "")).lower()]


def format_transaction(transaction: dict) -> str:
    """Форматирует транзакцию для вывода."""
    date = transaction.get("date", "N/A")
    description = transaction.get("description", "N/A")
    amount = transaction.get("amount", "N/A")
    currency = transaction.get("currency", "N/A")

    return f"{date} {description} Сумма: {amount} {currency}"
