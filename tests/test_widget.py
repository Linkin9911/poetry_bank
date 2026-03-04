import os
import sys

import pytest
from src.widget import mask_account_card  # Только импорт, без локального определения


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# Все тесты остаются без изменений — они используют импортированную функцию
@pytest.mark.parametrize(
    "input_data,expected_type,expected_output",
    [
        ("Visa 1234567890123456", "card", "Visa 1234 56** **** 3456"),
        ("Account 7365487623487654", "account", "Account **7654"),
        ("", "unknown", "Некорректные входные данные"),
        ("Invalid data abc", "unknown", "Invalid data abc Введён некорректный номер карты"),
    ],
)
def test_mask_account_card_basic(input_data: str, expected_type: str, expected_output: str) -> None:
    result = mask_account_card(input_data)
    assert result == expected_output


@pytest.mark.parametrize(
    "card_input,expected_output",
    [
        ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
        ("AmericanExpress 123456789012345", "AmericanExpress 1234 56** **** 345"),  # 15 цифр
        ("Discover 9999888877776666", "Discover 9999 88** **** 6666"),
    ],
)
def test_mask_account_card_cards(card_input: str, expected_output: str) -> None:
    """Тестирует маскировку разных типов карт."""
    result = mask_account_card(card_input)
    assert result == expected_output


@pytest.mark.parametrize(
    "account_input,expected_output",
    [
        ("Account 12345678901234567890", "Account **7890"),
        ("Savings 98765432109876543210", "Savings **3210"),
        ("Current 11112222333344445555", "Current **5555"),
    ],
)
def test_mask_account_card_accounts(account_input: str, expected_output: str) -> None:
    """Тестирует маскировку разных типов счетов."""
    result = mask_account_card(account_input)
    assert result == expected_output


def test_mask_account_card_empty_string() -> None:
    """Тестирует обработку пустой строки."""
    result = mask_account_card("")
    assert result == "Некорректные входные данные"


@pytest.mark.parametrize(
    "invalid_input,expected_output",
    [
        ("123456789012345", "123456789012345 Введён некорректный номер карты"),  # короткий номер карты
        ("736548762348765", "736548762348765 Введён некорректный номер счёта"),  # короткий номер счёта
        ("Visa abcdefghijklmno", "Visa abcdefghijklmno Введён некорректный номер карты"),  # буквы вместо цифр
        ("Account abcdefghijklmno", "Account abcdefghijklmno Введён некорректный номер счёта"),  # буквы вместо цифр
    ],
)
def test_mask_account_card_invalid_inputs(invalid_input: str, expected_output: str) -> None:
    """Тестирует обработку некорректных входных данных."""
    result = mask_account_card(invalid_input)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_with_spaces,expected_output",
    [
        (" Visa 1234567890123456 ", "Visa 1234 56** **** 3456"),
        (" Account 7365487623487654 ", "Account **7654"),
        ("  Invalid data abc  ", "Invalid data abc Введён некорректный номер карты"),
    ],
)
def test_mask_account_card_with_spaces(input_with_spaces: str, expected_output: str) -> None:
    """Тестирует обработку строк с пробелами."""
    result = mask_account_card(input_with_spaces)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_with_special_chars,expected_output",
    [
        ("Visa# 1234-5678-9012-3456", "Visa# 1234 56** **** 3456"),
        ("Account@ 7365 4876 2348 7654", "Account@ **7654"),
    ],
)
def test_mask_account_card_with_special_chars(input_with_special_chars: str, expected_output: str) -> None:
    """Тестирует обработку строк со спецсимволами."""
    result = mask_account_card(input_with_special_chars)
    assert result == expected_output


def test_mask_account_card_long_string() -> None:
    """Тестирует обработку длинной строки с номером карты/счёта."""
    long_input = "Очень длинная строка с номером карты Visa 1234567890123456"
    expected = "Очень длинная строка с номером карты Visa 1234 56** **** 3456"
    result = mask_account_card(long_input)
    assert result == expected
