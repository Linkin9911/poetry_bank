from typing import Any
from typing import Dict
from typing import List

import pytest

from src.data_processor import process_bank_operations
from src.data_processor import process_bank_search


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    """Возвращает тестовые данные для использования в тестах."""
    return [
        {"description": "Покупка в магазине", "status": "EXECUTED"},
        {"description": "Оплата интернета", "status": "CANCELED"},
        {"description": "Перевод другу", "status": "PENDING"},
    ]


def test_process_bank_search_found(sample_data: List[Dict[str, Any]]) -> None:
    """Тест поиска транзакции по ключевому слову (найдена)."""
    result = process_bank_search(sample_data, "магазин")
    assert len(result) == 1
    assert result[0]["description"] == "Покупка в магазине"


def test_process_bank_search_not_found(sample_data: List[Dict[str, Any]]) -> None:
    """Тест поиска транзакции (не найдена)."""
    result = process_bank_search(sample_data, "не существующее слово")
    assert len(result) == 0


def test_process_bank_search_empty_string(sample_data: List[Dict[str, Any]]) -> None:
    """Тест поиска с пустой строкой (возвращает все данные)."""
    result = process_bank_search(sample_data, "")
    assert result == sample_data  # При пустой строке возвращается весь список


def test_process_bank_operations_basic(sample_data: List[Dict[str, Any]]) -> None:
    """Базовый тест обработки банковских операций."""
    categories = ["Покупка", "Перевод"]
    result = process_bank_operations(sample_data, categories)
    assert "Покупка" in result
    assert "Перевод" in result
    assert result["Покупка"] == 1
    assert result["Перевод"] == 1


def test_process_bank_operations_case_insensitive(sample_data: List[Dict[str, Any]]) -> None:
    """Тест обработки операций без учёта регистра."""
    # Добавляем транзакцию с описанием в другом регистре
    extended_data = sample_data + [{"description": "покупка продуктов", "status": "EXECUTED"}]
    categories = ["покупка"]
    result = process_bank_operations(extended_data, categories)
    assert result.get("покупка", 0) == 2  # Должны найти оба варианта


def test_process_bank_operations_empty_categories(sample_data: List[Dict[str, Any]]) -> None:
    """Тест с пустым списком категорий."""
    result = process_bank_operations(sample_data, [])
    assert result == {}


def test_process_bank_operations_no_matches(sample_data: List[Dict[str, Any]]) -> None:
    """Тест с категориями, которых нет в данных."""
    categories = ["не существующая категория"]
    result = process_bank_operations(sample_data, categories)
    assert result["не существующая категория"] == 0
