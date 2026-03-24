from unittest.mock import patch
import pandas as pd
from src.data_reader import read_transactions_from_csv, read_transactions_from_excel

@patch('pandas.read_csv')
def test_read_transactions_from_csv_success(mock_read_csv):
    """Тест успешного чтения CSV-файла."""
    # Подготавливаем тестовые данные
    test_data = pd.DataFrame([
        {'id': 1, 'amount': 100, 'currency': 'RUB'},
        {'id': 2, 'amount': 200, 'currency': 'USD'}
    ])
    mock_read_csv.return_value = test_data

    # Вызываем тестируемую функцию
    result = read_transactions_from_csv('test.csv')

    # Проверяем результат
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[1]['amount'] == 200

@patch('pandas.read_csv')
def test_read_transactions_from_csv_error(mock_read_csv):
    """Тест обработки ошибки при чтении CSV-файла."""
    mock_read_csv.side_effect = Exception("File not found")

    result = read_transactions_from_csv('nonexistent.csv')
    assert result == []

@patch('pandas.read_excel')
def test_read_transactions_from_excel_success(mock_read_excel):
    """Тест успешного чтения Excel-файла."""
    test_data = pd.DataFrame([
        {'transaction_id': 'T001', 'sum': 500},
        {'transaction_id': 'T002', 'sum': 750}
    ])
    mock_read_excel.return_value = test_data

    result = read_transactions_from_excel('test.xlsx')

    assert len(result) == 2
    assert result[0]['transaction_id'] == 'T001'

@patch('pandas.read_excel')
def test_read_transactions_from_excel_error(mock_read_excel):
    """Тест обработки ошибки при чтении Excel-файла."""
    mock_read_excel.side_effect = Exception("Invalid file format")

    result = read_transactions_from_excel('invalid.xlsx')
    assert result == []

def test_read_csv_with_real_file():
    """Тест чтения реального CSV‑файла из папки data."""
    transactions = read_transactions_from_csv('data/transactions.csv')
    assert len(transactions) > 0, "CSV‑файл должен содержать хотя бы одну транзакцию"

def test_read_excel_with_real_file():
    """Тест чтения реального Excel‑файла из папки data."""
    transactions = read_transactions_from_excel('data/transactions_excel.xlsx')
    assert len(transactions) > 0, "Excel‑файл должен содержать хотя бы одну транзакцию"
