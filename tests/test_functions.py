# tests/test_functions.py
import unittest
from typing import Dict
from unittest.mock import mock_open
from unittest.mock import patch

from src.external_api import convert_to_rubles
from src.utils import read_json_file


class TestUtils(unittest.TestCase):

    @patch("os.path.exists", return_value=True)  # Гарантируем, что файл «существует»
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_read_empty_json(self, mock_file: unittest.mock.MagicMock, mock_exists: unittest.mock.MagicMock) -> None:
        result = read_json_file("dummy_path")
        self.assertEqual(result, [])
        mock_file.assert_called_once()  # Теперь вызов будет зафиксирован
        mock_exists.assert_called_with("dummy_path")  # Проверяем вызов exists

    @patch("os.path.exists")
    def test_file_not_found(self, mock_exists: unittest.mock.MagicMock) -> None:
        mock_exists.return_value = False
        result = read_json_file("nonexistent_file")
        self.assertEqual(result, [])
        mock_exists.assert_called_with("nonexistent_file")


class TestExternalAPI(unittest.TestCase):
    @patch("requests.get")
    def test_convert_usd_to_rub(self, mock_get: unittest.mock.MagicMock) -> None:
        mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}
        transaction: Dict[str, float | str] = {"amount": 10, "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 900.0)

    def test_rub_no_conversion(self) -> None:
        transaction: Dict[str, float | str] = {"amount": 1000, "currency": "RUB"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 1000.0)


if __name__ == "__main__":
    unittest.main()
