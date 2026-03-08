from src.masks import get_mask_account
from src.masks import get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"  # если поддерживается int
    assert get_mask_card_number("123") == "Введён некорректный номер карты"


def test_get_mask_account() -> None:
    assert get_mask_account("12345678901234567890") == "**7890"
    assert get_mask_account(12345678901234567890) == "**7890"  # если поддерживается int
    assert get_mask_account("123") == "Введён некорректный номер счёта"
