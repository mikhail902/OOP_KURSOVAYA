import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from src.api_connectors import HHruConnector


class TestHHruConnector(unittest.TestCase):

    def setUp(self):
        """Сетап для тестов"""
        self.connector = HHruConnector()
        self.connector.__base_url = "https://api.hh.ru/vacancies"
        if not hasattr(self.connector, "init"):
            self.connector.init = lambda self: None

    @patch("src.api_connectors.requests.get")
    def test_get_vacancies_success(self, mock_get):
        """Проверяет успешное получение вакансий."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Test Vacancy"}]}
        mock_get.return_value = mock_response

        vacancies = self.connector.get_vacancies("test")

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["name"], "Test Vacancy")

        mock_get.assert_called_once_with(
            self.connector.__base_url,
            params={"text": "test", "area": 113, "per_page": 100},
        )

    @patch("src.api_connectors.requests.get")
    def test_get_vacancies_api_error(self, mock_get):
        """Проверяет обработку ошибки API."""

        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        vacancies = self.connector.get_vacancies("test")

        self.assertEqual(len(vacancies), 0)

    @patch("src.api_connectors.requests.get")
    def test_get_vacancies_empty_response(self, mock_get):
        """Проверяет обработку пустого ответа от API."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        vacancies = self.connector.get_vacancies("test")

        self.assertEqual(len(vacancies), 0)

    @patch("src.api_connectors.requests.get")
    def test_send_request_success(self, mock_get):
        """Проверяет успешную отправку запроса."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.connector._HHruConnector__send_request(
            "https://api.example.com", {}
        )

        self.assertEqual(response.status_code, 200)

    @patch("src.api_connectors.requests.get")
    def test_send_request_http_error(self, mock_get):
        """Проверяет обработку HTTP ошибки."""

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "HTTP Error"
        )
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.connector._HHruConnector__send_request("https://api.example.com", {})


if __name__ == "__main__":
    unittest.main()
