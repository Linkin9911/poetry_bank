import pandas as pd
from typing import List, Dict
import os

def read_transactions_from_csv(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из CSV‑файла.

    Args:
        file_path (str): Путь к CSV‑файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями.
    """
    # Проверка существования файла
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    try:
        # Явно указываем кодировку и обработку плохих строк для надёжности
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            on_bad_lines='skip'  # Пропускаем строки с ошибками форматирования
        )
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка чтения CSV‑файла: {e}")
        return []

def read_transactions_from_excel(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel‑файла.

    Args:
        file_path (str): Путь к Excel‑файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями.
    """
    # Проверка существования файла
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    try:
        # Используем правильный движок 'openpyxl'
        df = pd.read_excel(
            file_path,
            engine='openpyxl'
        )
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка чтения Excel‑файла: {e}")
        return []
