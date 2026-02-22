from typing import Any
from typing import Dict
from typing import List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по значению ключа 'state'.

    Args:
        transactions: Список словарей с транзакциями.
        state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        Список словарей, где 'state' соответствует указанному значению.
    """
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список транзакций по дате ('date').

    Args:
        transactions: Список словарей с транзакциями.
        reverse: Если True — сортировка по убыванию (по умолчанию).

    Returns:
        Отсортированный список транзакций."""
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
