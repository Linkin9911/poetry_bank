from typing import Dict
from typing import List

import pytest

from src.utils import filter_by_status
from src.utils import filter_ruble_transactions
from src.utils import format_transaction
from src.utils import sort_by_date


@pytest.fixture
def sample_data() -> List[Dict]:
    """Возвращает тестовые данные для использования в тестах."""
    return [
        {
            "date": "2023-01-01",
            "description": "Оплата интернета",
            "amount": 500,
            "currency": "руб",
            "status": "EXECUTED",
        },
        {
            "date": "2023-01-02",
            "description": "Перевод другу",
            "amount": 1000,
            "currency": "USD",
            "status": "CANCELED",
        },
        {
            "date": "2023-01-03",
            "description": "Покупка в магазине",
            "amount": 300,
            "currency": "руб",
            "status": "PENDING",
        },
    ]


def test_filter_by_status_basic(sample_data: List[Dict]) -> None:
    """Тест базовой фильтрации по статусу."""
    result = filter_by_status(sample_data, "EXECUTED")
    assert len(result) == 1
    assert result[0]["status"] == "EXECUTED"


def test_filter_by_status_case_insensitive(sample_data: List[Dict]) -> None:
    """Тест фильтрации по статусу без учёта регистра."""
    result = filter_by_status(sample_data, "executed")
    assert len(result) == 1  # Должен найти, несмотря на регистр


def test_sort_by_date_ascending(sample_data: List[Dict]) -> None:
    """Тест сортировки по дате по возрастанию."""
    sorted_data = sort_by_date(sample_data, ascending=True)
    dates = [t["date"] for t in sorted_data]
    assert dates == sorted(dates)  # Даты должны быть отсортированы по возрастанию


def test_sort_by_date_descending(sample_data: List[Dict]) -> None:
    """Тест сортировки по дате по убыванию."""
    sorted_data = sort_by_date(sample_data, ascending=False)
    dates = [t["date"] for t in sorted_data]
    assert dates == sorted(dates, reverse=True)  # По убыванию


def test_filter_ruble_transactions_basic(sample_data: List[Dict]) -> None:
    """Тест фильтрации рублёвых транзакций."""
    result = filter_ruble_transactions(sample_data)
    assert len(result) == 2  # Две рублёвые транзакции
    for transaction in result:
        assert "руб" in transaction["currency"].lower()


def test_format_transaction_basic() -> None:
    """Тест форматирования транзакции."""
    transaction = {"date": "01.01.2023", "description": "Оплата интернета", "amount": 500, "currency": "руб"}
    formatted = format_transaction(transaction)
    expected = "01.01.2023 Оплата интернета Сумма: 500 руб"
    assert formatted == expected
