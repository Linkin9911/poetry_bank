from typing import Any  # Импортируем Any для аннотаций типов
from unittest.mock import patch

import pandas as pd

from src.data_reader import read_transactions_from_csv
from src.data_reader import read_transactions_from_excel


@patch("pandas.read_csv")
def test_read_transactions_from_csv_success(mock_read_csv: Any) -> None:
    """Тест успешного чтения CSV‑файла."""
    # Используем mock: задаём возвращаемое значение
    test_data = pd.DataFrame(
        [{"id": 1, "amount": 100, "currency": "RUB"}, {"id": 2, "amount": 200, "currency": "USD"}]
    )
    mock_read_csv.return_value = test_data

    result = read_transactions_from_csv("test.csv")
    assert len(result) == 2


@patch("pandas.read_excel")
def test_read_transactions_from_excel_success(mock_read_excel: Any) -> None:
    """Тест успешного чтения Excel‑файла."""
    # Используем mock: задаём возвращаемое значение
    test_data = pd.DataFrame([{"transaction_id": "T001", "sum": 500}, {"transaction_id": "T002", "sum": 750}])
    mock_read_excel.return_value = test_data

    result = read_transactions_from_excel("test.xlsx")
    assert len(result) == 2


@patch("pandas.read_csv", side_effect=Exception("Ошибка чтения"))
def test_read_transactions_from_csv_failure(mock_read_csv: Any) -> None:
    """Тест обработки ошибки при чтении CSV‑файла."""
    result = read_transactions_from_csv("broken.csv")
    assert result == []
