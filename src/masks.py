from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Маскирует номер банковской карты по шаблону 'XXXX XX** **** XXXX'.


    Оставляет видимыми:
    - первые 4 цифры номера карты;
    - две цифры после первых четырёх (в формате 'XX**');
    - последние 4 цифры.

    Остальные цифры заменяются на звёздочки."""
    card_str = str(card_number).strip()
    if len(card_str) != 16 or not card_str.isdigit():
        return "Введён некорректный номер карты"
    return f"{card_str[0:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счёта, оставляя видимыми только последние 4 цифры.

    Формат вывода: '**XXXX', где XXXX — последние 4 цифры номера счёта."""
    acc_str = str(account_number).strip()
    if len(acc_str) != 20 or not acc_str.isdigit():
        return "Введён некорректный номер счёта"
    return f"**{acc_str[-4:]}"
