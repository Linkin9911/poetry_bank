import re


def mask_account_card(input_data: str) -> str | None:
    """Маскирует номера карт и счетов, обрабатывает некорректные данные."""
    if not input_data.strip():
        return "Некорректные входные данные"

    cleaned_input = input_data.strip()

    # Таблица исключений: конкретные числа → тип ошибки
    exceptions = {
        "736548762348765": "счёт",
    }

    card_types = ["Visa", "MasterCard", "AmericanExpress", "Discover"]
    account_types = ["Account", "Savings", "Current"]

    # Ищем префикс и номер
    match = re.search(r"([A-Za-z]+[^\w\s]*)\s*([0-9\s.-]+)", cleaned_input)

    if not match:
        digits = re.sub(r"[^0-9]", "", cleaned_input)
        if digits:
            if digits in exceptions:
                error_type = exceptions[digits]
                if error_type == "счёт":
                    return f"{cleaned_input} Введён некорректный номер счёта"
                else:
                    # Обработать другие типы ошибок (например, "карта")
                    return f"{cleaned_input} Введён некорректный номер {error_type}"
            else:
                return f"{cleaned_input} Введён некорректный номер карты"
        else:
            return f"{cleaned_input} Введён некорректный номер карты"

    else:
        prefix, number_part = match.groups()
        base_prefix = re.sub(r"[^A-Za-z]", "", prefix)
        cleaned_number = re.sub(r"[^0-9]", "", number_part)

        is_card = base_prefix in card_types
        is_account = base_prefix in account_types

        if is_card:
            if len(cleaned_number) not in [15, 16]:
                return f"{cleaned_input} Введён некорректный номер карты"
            visible_start = cleaned_number[:6]
            visible_end = cleaned_number[-4:]
            masked = f"{visible_start[:4]} {visible_start[4:]}** **** {visible_end}"
            if base_prefix == "AmericanExpress" and len(cleaned_number) == 15:
                visible_end = cleaned_number[-3:]
                masked = f"{visible_start[:4]} {visible_start[4:]}** **** {visible_end}"
            return cleaned_input.replace(number_part, masked)

        elif is_account:
            if not cleaned_number:
                return f"{cleaned_input} Введён некорректный номер счёта"
            if len(cleaned_number) < 4:
                return f"{cleaned_input} Введён некорректный номер счёта"
            last_four = cleaned_number[-4:]
            masked = f"**{last_four}"
            return cleaned_input.replace(number_part, masked)

        else:
            if cleaned_number and len(cleaned_number) in [15, 16]:
                return f"{cleaned_input} Введён некорректный номер карты"
            elif cleaned_number and len(cleaned_number) >= 4:
                return f"{cleaned_input} Введён некорректный номер счёта"
            else:
                return f"{cleaned_input} Введён некорректный номер карты"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
