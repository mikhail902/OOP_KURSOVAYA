import json
import os
import sys
import unittest
from unittest.mock import mock_open, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from src.data_savers import DataSaver, JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver(unittest.TestCase):
    TEST_FILENAME = "test_vacancies.json"

    def setUp(self):
        """Сетап для тестов"""
        self.saver = JSONSaver()
        self.saver.filename = self.TEST_FILENAME

        self.saver.__init__(filename=self.TEST_FILENAME)

        self.saver.data = []
        self.mock_file = None

    def tearDown(self):
        """Выход"""
        if os.path.exists(self.TEST_FILENAME):
            os.remove(self.TEST_FILENAME)

    @patch("src.data_savers.open", new_callable=mock_open, read_data="[]")
    def test_load_data_empty_file(self, mock_open_func):
        """Проверяет загрузку данных из пустого файла."""
        self.saver.filename = "empty_test_file.json"
        data = self.saver._JSONSaver__load_data()
        self.assertEqual(data, [])

    @patch("src.data_savers.open", side_effect=FileNotFoundError)
    def test_load_data_file_not_found(self, mock_open_func):
        """Проверяет обработку исключения FileNotFoundError."""
        self.saver.filename = "nonexistent_file.json"
        data = self.saver._JSONSaver__load_data()
        self.assertEqual(data, [])

    @patch("src.data_savers.open", new_callable=mock_open, read_data="invalid json")
    def test_load_data_invalid_json(self, mock_open_func):
        """Проверяет обработку исключения JSONDecodeError."""
        self.saver.filename = "invalid_json_file.json"
        data = self.saver._JSONSaver__load_data()
        self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()
