from datetime import datetime

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счёта в зависимости от типа входных данных.


    Args:
        info (str): Строка вида "Visa Platinum 7000..." или "Счёт 7365...".


    Returns:
        str: Строка с замаскированным номером. Для карт — формат
        "XXXX XX** **** XXXX", для счетов — "**XXXX".
    """
    parts = info.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.strip().lower().startswith(("счёт", "счет")):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Преобразует дату из формата '2024-03-11T02:26:18.671407'
    в формат '11.03.2024'.

    Args:
        date_str (str): Дата в формате ISO с разделителем 'T'.


    Returns:
        str: Дата в формате 'ДД.ММ.ГГГГ' или сообщение об ошибке.
    """
    try:
        dt = datetime.fromisoformat(date_str.replace("T", " "))
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return "Некорректный формат даты"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
