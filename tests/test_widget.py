import os
import sys

import pytest

from src.widget import mask_account_card

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.mark.parametrize(
    "input_data,expected_type,expected_output",
    [
        ("Visa 1234567890123456", "card", "Visa 1234 56** **** 3456"),
        ("Account 7365487623487654", "account", "Account **7654"),
        ("", "unknown", "Некорректные входные данные"),
        ("Invalid data abc", "unknown", "Invalid data abc Введён некорректный номер карты"),
    ],
)
def test_mask_account_card(input_data: str, expected_type: str, expected_output: str) -> None:
    result = mask_account_card(input_data)
    assert result == expected_output
