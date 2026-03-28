import json
from typing import Dict
from typing import List
from typing import Union

from src.data_processor import process_bank_search
from src.utils import filter_by_status
from src.utils import filter_ruble_transactions
from src.utils import format_transaction
from src.utils import sort_by_date


def main() -> None:
    """Основная функция программы с пользовательским интерфейсом."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice != "1":
        print("Программа: В демо-версии доступен только JSON-файл.")

    print("Программа: Для обработки выбран JSON-файл.")

    # Загрузка данных
    try:
        with open("../data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Файл data.json не найден. Создаю тестовые данные.")
        data = create_sample_data()

    # Фильтрация по статусу с повторным запросом при ошибке
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    status = None  # Инициализируем переменную заранее

    while status is None:
        print(f"Программа: Доступные для фильтрации статусы: {', '.join(valid_statuses)}")
        status_input = input("Программа: Введите статус операции: ").strip().upper()

        if not status_input:  # Проверка на пустой ввод
            print("Программа: Статус не может быть пустым. Попробуйте ещё раз.")
            continue

        if status_input in valid_statuses:
            status = status_input
            print(f"Программа: Операции отфильтрованы по статусу '{status}'")
        else:
            print(f"Программа: Статус операции '{status_input}' недоступен. " "Пожалуйста, выберите из списка выше.")

    filtered_data = filter_by_status(data, status)

    # Сортировка по дате
    while True:
        sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
        if sort_choice in ("да", "нет"):
            break
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'.")

    if sort_choice == "да":
        while True:
            order = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
            if "возрастанию" in order:
                ascending = True
                break
            elif "убыванию" in order:
                ascending = False
                break
            else:
                print("Программа: Пожалуйста, введите 'возрастанию' или 'убыванию'.")
        filtered_data = sort_by_date(filtered_data, ascending)

    # Фильтрация рублёвых транзакций
    while True:
        ruble_choice = input("Программа: Выводить только рублёвые транзакции? Да/Нет\nПользователь: ").strip().lower()
        if ruble_choice in ("да", "нет"):
            break
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'.")

    if ruble_choice == "да":
        filtered_data = filter_ruble_transactions(filtered_data)

    # Поиск по описанию
    while True:
        search_choice = (
            input(
                "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\nПользователь: "
            )
            .strip()
            .lower()
        )
        if search_choice in ("да", "нет"):
            break
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'.")

    if search_choice == "да":
        search_term = input("Программа: Введите слово для поиска: ").strip()
        if search_term:  # Только если введено непустое слово
            filtered_data = process_bank_search(filtered_data, search_term)
        else:
            print("Программа: Слово для поиска не введено. Пропускаем фильтрацию.")

    # Вывод результата
    print("Программа: Распечатываю итоговый список транзакций...")
    if filtered_data:
        print(f"Программа: Всего банковских операций в выборке: {len(filtered_data)}")
        for transaction in filtered_data:
            print(format_transaction(transaction))
    else:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


def create_sample_data() -> List[Dict[str, Union[str, int]]]:
    """Создаёт тестовые данные для демонстрации."""
    return [
        {
            "date": "08.12.2019",
            "description": "Открытие вклада",
            "amount": 40542,
            "currency": "руб",
            "status": "EXECUTED",
        },
        {
            "date": "12.11.2019",
            "description": "Перевод с карты на карту",
            "amount": 130,
            "currency": "USD",
            "status": "EXECUTED",
        },
    ]


if __name__ == "__main__":
    main()
