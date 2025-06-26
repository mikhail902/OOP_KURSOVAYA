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

    def test_add_vacancy(self):
        """Проверяет добавление вакансии."""
        vacancy = Vacancy("Test Title", "http://test.com", 100, 200, "Test Description")
        self.saver.add_vacancy(vacancy)
        self.assertEqual(len(self.saver.data), 1)
        self.assertEqual(self.saver.data[0]["title"], "Test Title")

    def test_add_duplicate_vacancy(self):
        """Проверяет предотвращение добавления дубликатов вакансий."""
        vacancy1 = Vacancy(
            "Test Title", "http://test.com", 100, 200, "Test Description"
        )
        vacancy2 = Vacancy(
            "Different Title", "http://test.com", 300, 400, "Different Description"
        )  # Тот же URL
        self.saver.add_vacancy(vacancy1)
        self.saver.add_vacancy(vacancy2)
        self.assertEqual(len(self.saver.data), 1)

    def test_get_vacancies_with_criteria(self):
        """Проверяет получение вакансий по критериям."""
        vacancy1 = Vacancy(
            "Test Title", "http://test.com", 100, 200, "Test Description"
        )
        vacancy2 = Vacancy(
            "Another Title", "http://another.com", 300, 400, "Another Description"
        )
        self.saver.add_vacancy(vacancy1)
        self.saver.add_vacancy(vacancy2)

        results = self.saver.get_vacancies({"title": "Test Title"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].url, "http://test.com")

        results = self.saver.get_vacancies({"title": "Nonexistent Title"})
        self.assertEqual(len(results), 0)

    def test_delete_vacancy(self):
        """Проверяет удаление вакансии."""
        vacancy1 = Vacancy(
            "Test Title", "http://test.com", 100, 200, "Test Description"
        )
        vacancy2 = Vacancy(
            "Another Title", "http://another.com", 300, 400, "Another Description"
        )
        self.saver.add_vacancy(vacancy1)
        self.saver.add_vacancy(vacancy2)
        self.assertEqual(len(self.saver.data), 2)

        self.saver.delete_vacancy(vacancy1)
        self.assertEqual(len(self.saver.data), 1)
        self.assertEqual(self.saver.data[0]["title"], "Another Title")

    def test_delete_nonexistent_vacancy(self):
        """Проверяет попытку удаления несуществующей вакансии."""
        vacancy1 = Vacancy(
            "Test Title", "http://test.com", 100, 200, "Test Description"
        )
        vacancy2 = Vacancy(
            "Nonexistent Title",
            "http://nonexistent.com",
            300,
            400,
            "Nonexistent Description",
        )
        self.saver.add_vacancy(vacancy1)
        initial_len = len(self.saver.data)

        self.saver.delete_vacancy(vacancy2)
        self.assertEqual(len(self.saver.data), initial_len)

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
