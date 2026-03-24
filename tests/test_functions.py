# tests/test_functions.py
import unittest
from typing import Dict
from typing import Union
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

from src.external_api import convert_to_rubles
from src.utils import read_json_file


class TestUtils(unittest.TestCase):
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_read_empty_json(self, mock_file: MagicMock, mock_exists: MagicMock) -> None:
        """Тест чтения пустого JSON-файла."""
        result = read_json_file("dummy_path")
        self.assertEqual(result, [])
        mock_file.assert_called_once()
        mock_exists.assert_called_with("dummy_path")

    @patch("os.path.exists")
    def test_file_not_found(self, mock_exists: MagicMock) -> None:
        """Тест обработки несуществующего файла."""
        mock_exists.return_value = False
        result = read_json_file("nonexistent_file")
        self.assertEqual(result, [])
        mock_exists.assert_called_with("nonexistent_file")


class TestExternalAPI(unittest.TestCase):
    @patch("requests.get")
    def test_convert_usd_to_rub(self, mock_get: MagicMock) -> None:
        """Тест конвертации USD в RUB через API."""
        # Настраиваем мок для имитации успешного ответа API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 900.0}
        mock_get.return_value.text = '{"result": 900.0}'

        transaction: Dict[str, Union[float, str]] = {"amount": 10, "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 900.0)

    def test_rub_no_conversion(self) -> None:
        """Тест случая, когда конвертация не нужна (валюта уже RUB)."""
        transaction: Dict[str, Union[float, str]] = {"amount": 1000, "currency": "RUB"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 1000.0)  # Конвертация не нужна, возвращаем исходную сумму


if __name__ == "__main__":
    unittest.main()
