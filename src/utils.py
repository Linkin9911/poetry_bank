import json
import logging
import os
from typing import Dict
from typing import List

# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# Создаём логер для модуля utils
logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)

# Настраиваем формат лога
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Настраиваем файловый хендлер (запись в файл) с кодировкой UTF-8
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setFormatter(file_formatter)

# Добавляем хендлер к логеру (с проверкой, чтобы избежать дублирования)
if not logger_utils.handlers:
    logger_utils.addHandler(file_handler)


def read_json_file(file_path: str) -> List[Dict]:
    """Читает JSON-файл и возвращает список словарей с данными о транзакциях."""
    logger_utils.info(f"Попытка прочитать файл: {file_path}")

    if not os.path.exists(file_path):
        logger_utils.error(f"Файл не найден: {file_path}")
        return []

    try:
        logger_utils.debug(f"Файл {file_path} открыт для чтения")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger_utils.info(f"Данные успешно загружены из {file_path}, получено {len(data)} записей")
                return data
            else:
                logger_utils.warning(
                    f"Данные из {file_path} не являются списком "
                    f"(тип: {type(data).__name__}), возвращаем пустой результат"
                )

                return []
    except json.JSONDecodeError as e:
        logger_utils.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except IOError as e:
        logger_utils.error(f"Ошибка ввода-вывода при чтении файла {file_path}: {str(e)}")
        return []
    finally:
        # Принудительно сбрасываем буфер логера после каждой операции
        for handler in logger_utils.handlers:
            handler.flush()


if __name__ == "__main__":
    print("Тестовый запуск функций utils.py...")
    print("Текущая рабочая директория:", os.getcwd())

    # Проверяем существование data.json
    if os.path.exists("data.json"):
        print("Файл data.json найден, читаем его...")
        result1 = read_json_file("data.json")
        print("Результат чтения корректного файла:", result1)
    else:
        print("Файл data.json НЕ найден в текущей директории!")
        print("Попробуйте создать его с содержимым:")
        print('[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]')

    result2 = read_json_file("nonexistent.json")
    print("Результат чтения несуществующего файла:", result2)
    print("Проверьте logs/utils.log — в нём должны быть записи!")
