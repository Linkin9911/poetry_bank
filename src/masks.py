import logging
import os
from typing import Union

# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# Создаём логер для модуля masks
logger_masks = logging.getLogger("masks")
logger_masks.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования не меньше DEBUG

# Настраиваем формат лога
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Настраиваем файловый хендлер (запись в файл) с кодировкой UTF-8
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setFormatter(file_formatter)

# Добавляем хендлер к логеру (с проверкой на дублирование)
if not logger_masks.handlers:
    logger_masks.addHandler(file_handler)


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Маскирует номер банковской карты по шаблону 'XXXX XX** **** XXXX'.

    Оставляет видимыми:
    - первые 4 цифры номера карты;
    - две цифры после первых четырёх (в формате 'XX**');
    - последние 4 цифры.

    Остальные цифры заменяются на звёздочки."""
    logger_masks.info(f"Попытка замаскировать номер карты: {card_number}")
    card_str = str(card_number).strip()
    logger_masks.debug(f"Преобразованный номер карты в строку: '{card_str}'")

    if len(card_str) != 16 or not card_str.isdigit():
        logger_masks.error(
            f"Некорректный номер карты: '{card_str}'. " f"Длина: {len(card_str)}, содержит цифры: {card_str.isdigit()}"
        )

        return "Введён некорректный номер карты"

    masked = f"{card_str[0:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    logger_masks.info(f"Номер карты успешно замаскирован: {masked}")
    return masked


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счёта, оставляя видимыми только последние 4 цифры.

    Формат вывода: '**XXXX', где XXXX — последние 4 цифры номера счёта."""
    logger_masks.info(f"Попытка замаскировать номер счёта: {account_number}")
    acc_str = str(account_number).strip()
    logger_masks.debug(f"Преобразованный номер счёта в строку: '{acc_str}'")

    if len(acc_str) != 20 or not acc_str.isdigit():
        logger_masks.error(
            f"Некорректный номер счёта: '{acc_str}'. " f"Длина: {len(acc_str)}, содержит цифры: {acc_str.isdigit()}"
        )

        return "Введён некорректный номер счёта"

    masked = f"**{acc_str[-4:]}"
    logger_masks.info(f"Номер счёта успешно замаскирован: {masked}")
    return masked


if __name__ == "__main__":
    # Вызываем функции — это запустит логирование
    print("Результат маскировки карты:", get_mask_card_number("1234567890123456"))
    print("Результат маскировки счёта:", get_mask_account("12345678901234567890"))
