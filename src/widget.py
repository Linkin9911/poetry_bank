from datetime import datetime


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счёта в зависимости от типа входных данных.
    Args:
        info (str): Строка вида "Visa Platinum 7000..." или "Счёт 7365...".
    Returns:
        str: Строка с замаскированным номером. Для карт — формат
        "XXXX XX** **** XXXX", для счетов — "**XXXX".
    """
    if not info or not info.strip():
        return "Некорректные входные данные"

    parts = info.split()
    if len(parts) < 2:
        return f"{info} Введён некорректный номер карты"

    number = parts[-1]

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        return f"{info} Введён некорректный номер карты"

    if "Счёт" in info or "Account" in info:
        # Для счетов — последние 4 цифры, остальное маскируем
        if len(number) >= 4:
            masked = "**" + number[-4:]
        else:
            masked = number
        return f"{' '.join(parts[:-1])} {masked}"

    else:
        # Для карт — стандартный формат маскировки
        if len(number) == 16 and number.isdigit():
            masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
            return f"{' '.join(parts[:-1])} {masked}"
        else:
            return f"{info} Введён некорректный номер карты"


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
