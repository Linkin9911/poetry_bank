import re
from collections import Counter
from typing import Dict
from typing import List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет транзакции по заданной строке в описании с использованием регулярных выражений.

    Args:
        data: список словарей с транзакциями
        search: строка для поиска в поле description

    Returns:
        Список словарей с операциями, содержащими строку поиска в описании
    """
    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        data: список словарей с транзакциями
        categories: список категорий для подсчёта

    Returns:
        Словарь с количеством операций для каждой категории
    """
    # Извлекаем описания всех транзакций
    descriptions = [t.get("description", "").lower() for t in data]

    # Считаем все описания
    counter = Counter(descriptions)

    # Формируем результат только для указанных категорий
    result = {}
    for category in categories:
        # Ищем описания, содержащие категорию (частичное совпадение)
        count = sum(counter[desc] for desc in counter if category.lower() in desc)
        result[category] = count

    return result
