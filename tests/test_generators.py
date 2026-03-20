from typing import Any
from typing import Dict
from typing import List

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


# Тесты для filter_by_currency
@pytest.mark.parametrize(
    "currency, expected_count",
    [("USD", 2), ("RUB", 1), ("EUR", 0)],
)
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency: str, expected_count: int) -> None:
    filtered = list(filter_by_currency(sample_transactions, currency))
    assert len(filtered) == expected_count


def test_filter_by_currency_empty_list() -> None:
    assert list(filter_by_currency([], "USD")) == []


# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = ["Перевод со счета на счет", "Перевод со счета на счет", "Перевод со счета на счет"]
    assert descriptions == expected


def test_transaction_descriptions_empty_list() -> None:
    assert list(transaction_descriptions([])) == []


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start: int, stop: int, expected: List[str]) -> None:
    generated = list(card_number_generator(start, stop))
    assert generated == expected


def test_card_number_generator_single_number() -> None:
    result = list(card_number_generator(5, 5))
    assert result == ["0000 0000 0000 0005"]
