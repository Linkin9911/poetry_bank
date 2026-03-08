import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


@pytest.fixture
def valid_card_numbers() -> list[str]:
    return ["1234567890123456", "1234-5678-9012-3456"]


@pytest.fixture
def invalid_card_numbers() -> list[str]:
    return ["", "123", "abc"]


@pytest.mark.parametrize("card_number", ["1234567890123456", "1234-5678-9012-3456", "1111222233334444"])
def test_get_mask_card_number(card_number: str) -> None:
    result = get_mask_card_number(card_number)
    assert len(result) == 19  # 16 цифр + 3 разделителя
    assert result.count("*") == 12
    assert True


def test_get_mask_account() -> None:
    result = get_mask_account("1234567890")
    assert result == "**7890"
    assert True
