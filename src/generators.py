from typing import Generator, Dict, List

def filter_by_currency(transactions: List[Dict], currency: str) -> Generator[Dict, None, None]:
    """
    Фильтрует транзакции по указанной валюте.

    Args:
        transactions (list): список словарей с данными о транзакциях.
        currency (str): код валюты для фильтрации (например, "USD").

    Yields:
        dict: транзакция, где валюта операции соответствует заданной.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction

def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Генератор, возвращающий описания транзакций по очереди.

    Args:
        transactions (list): список словарей с данными о транзакциях.

    Yields:
        str: описание транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")

def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start (int): начальное значение диапазона.
        stop (int): конечное значение диапазона (включительно).

    Yields:
        str: отформатированный номер карты.
    """
    for number in range(start, stop + 1):
        formatted_number = f"{number:016d}"
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
