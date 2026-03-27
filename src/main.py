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

    # Загрузка данных (в реальной версии здесь будет выбор файла)
    try:
        with open("../data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Файл data.json не найден. Создаю тестовые данные.")
        data = create_sample_data()

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input("Пользователь: ").upper()
        print(f"Программа: Операции отфильтрованы по статусу '{status}'")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")

        if status in valid_statuses:
            break
        else:
            print(f"Программа: Статус операции '{status}' недоступен.")

    filtered_data = filter_by_status(data, status)
    print(f"Программа: Операции отфильтрованы по статусу '{status}'")

    # Сортировка по дате
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ").lower()
    if sort_choice == "да":
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").lower()
        ascending = "возрастанию" in order
        filtered_data = sort_by_date(filtered_data, ascending)

    # Фильтрация рублёвых транзакций
    ruble_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").lower()
    if ruble_choice == "да":
        filtered_data = filter_ruble_transactions(filtered_data)

    # Поиск по описанию
    search_choice = input(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\nПользователь: "
    ).lower()
    if search_choice == "да":
        search_term = input("Введите слово для поиска: ")
        filtered_data = process_bank_search(filtered_data, search_term)

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
