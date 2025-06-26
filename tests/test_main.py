import io
import os
import sys
import unittest
from unittest.mock import MagicMock, call, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from src.api_connectors import HHruConnector
from src.data_savers import JSONSaver
from src.main import interact_with_user
from src.vacancy import Vacancy


class TestInteractWithUser(unittest.TestCase):

    @patch("src.main.input", side_effect=["6"])
    def test_exit_program(self, mock_input):
        """Проверяет выход из программы."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            interact_with_user(json_saver_mock, hh_connector_mock)
        self.assertIn("Выход из программы.", stdout.getvalue())

    @patch("src.main.input", side_effect=["1", "test query", "6"])
    def test_search_vacancies(self, mock_input):
        """Проверяет поиск вакансий на hh.ru."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        hh_connector_mock.get_vacancies.return_value = [
            {
                "name": "Test Vacancy",
                "alternate_url": "http://test.com",
                "salary": {"from": 100, "to": 200},
                "snippet": {"requirement": "Test requirement"},
            }
        ]
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            interact_with_user(json_saver_mock, hh_connector_mock)
        hh_connector_mock.get_vacancies.assert_called_once_with("test query")
        json_saver_mock.add_vacancy.assert_called_once()
        self.assertIn("Test Vacancy", stdout.getvalue())

    @patch("src.main.input", side_effect=["2", "2", "6"])
    def test_get_top_n_vacancies(self, mock_input):
        """Проверяет получение топ N вакансий по зарплате."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        vacancy1 = Vacancy(
            "Test Title1",
            "http://test1.com",
            salary_from=200,
            salary_to=300,
            description="Test Description1",
        )
        vacancy2 = Vacancy(
            "Test Title2",
            "http://test2.com",
            salary_from=100,
            salary_to=200,
            description="Test Description2",
        )
        json_saver_mock.get_vacancies.return_value = [vacancy1, vacancy2]
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            interact_with_user(json_saver_mock, hh_connector_mock)
        json_saver_mock.get_vacancies.assert_called_once_with({})
        self.assertIn("Test Title1", stdout.getvalue())
        self.assertIn("Test Title2", stdout.getvalue())

    @patch("src.main.input", side_effect=["3", "keyword", "6"])
    def test_search_by_keyword(self, mock_input):
        """Проверяет поиск вакансий по ключевому слову в описании."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        vacancy1 = Vacancy(
            "Test Title1",
            "http://test1.com",
            salary_from=200,
            salary_to=300,
            description="Test Description with keyword",
        )
        vacancy2 = Vacancy(
            "Test Title2",
            "http://test2.com",
            salary_from=100,
            salary_to=200,
            description="Test Description2",
        )
        json_saver_mock.get_vacancies.return_value = [vacancy1, vacancy2]
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            interact_with_user(json_saver_mock, hh_connector_mock)
        json_saver_mock.get_vacancies.assert_called_once_with({})
        self.assertIn("Test Title1", stdout.getvalue())
        self.assertNotIn("Test Title2", stdout.getvalue())

    @patch("src.main.input", side_effect=["4", "6"])
    def test_display_all_vacancies(self, mock_input):
        """Проверяет вывод всех сохраненных вакансий."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        vacancy1 = Vacancy(
            "Test Title1",
            "http://test1.com",
            salary_from=200,
            salary_to=300,
            description="Test Description1",
        )
        vacancy2 = Vacancy(
            "Test Title2",
            "http://test2.com",
            salary_from=100,
            salary_to=200,
            description="Test Description2",
        )
        json_saver_mock.get_vacancies.return_value = [vacancy1, vacancy2]
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            interact_with_user(json_saver_mock, hh_connector_mock)
        json_saver_mock.get_vacancies.assert_called_once_with({})
        self.assertIn("Test Title1", stdout.getvalue())
        self.assertIn("Test Title2", stdout.getvalue())

    @patch("src.main.input", side_effect=["5", "http://test.com", "6"])
    def test_delete_vacancy(self, mock_input):
        """Проверяет удаление вакансии."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        interact_with_user(json_saver_mock, hh_connector_mock)
        json_saver_mock.delete_vacancy.assert_called_once()

    @patch("src.main.input", side_effect=["7", "6"])
    def test_invalid_choice(self, mock_input):
        """Проверяет обработку неверного выбора."""
        json_saver_mock = MagicMock(spec=JSONSaver)
        hh_connector_mock = MagicMock(spec=HHruConnector)
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            interact_with_user(json_saver_mock, hh_connector_mock)
        self.assertIn(
            "Неверный выбор. Пожалуйста, выберите действие из списка.",
            stdout.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
