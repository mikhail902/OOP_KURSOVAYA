import json
import os
from typing import Dict, List, Union
from unittest.mock import MagicMock, patch

import pytest

# Import your original code here
from src.main import (
    APIConnector,  # Make sure your classes are accessible
    HHruConnector,
    JSONSaver,
    Vacancy,
)


class TestAPIConnector:
    def test_api_connector_abstract_methods(self):
        with pytest.raises(TypeError):
            APIConnector()


class TestHHruConnector:
    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Test Vacancy",
                    "alternate_url": "test_url",
                    "salary": {"from": 100, "to": 200},
                }
            ]
        }
        mock_get.return_value = mock_response

        connector = HHruConnector()
        vacancies = connector.get_vacancies("test")
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Test Vacancy"
        mock_get.assert_called_once()


class TestVacancy:
    def test_vacancy_creation(self):
        vacancy = Vacancy("Test Vacancy", "test_url", 100, 200, "Test Description")
        assert vacancy.title == "Test Vacancy"
        assert vacancy.salary_from == 100

    def test_vacancy_comparison(self):
        vacancy1 = Vacancy("Test Vacancy", "test_url", 100, 200, "Test Description")
        vacancy2 = Vacancy("Test Vacancy", "test_url", 200, 300, "Test Description")
        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert not (vacancy1 == vacancy2)

    def test_vacancy_no_salary(self):
        vacancy = Vacancy("Test Vacancy", "test_url")
        assert vacancy.salary_from == 0


class TestJSONSaver:
    TEST_FILENAME = "test_vacancies.json"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.saver = JSONSaver(filename=self.TEST_FILENAME)
        self.test_vacancy = Vacancy(
            "Test Vacancy", "test_url", 100, 200, "Test Description"
        )
        yield  # Execute tests
        if os.path.exists(self.TEST_FILENAME):
            os.remove(self.TEST_FILENAME)

    def test_add_vacancy(self):
        self.saver.add_vacancy(self.test_vacancy)
        loaded_data = self.saver._JSONSaver__load_data()
        assert len(loaded_data) == 1
        assert loaded_data[0]["title"] == "Test Vacancy"

    def test_get_vacancies(self):
        self.saver.add_vacancy(self.test_vacancy)
        vacancies = self.saver.get_vacancies({"title": "Test Vacancy"})
        assert len(vacancies) == 1
        assert vacancies[0].title == "Test Vacancy"

    def test_delete_vacancy(self):
        self.saver.add_vacancy(self.test_vacancy)
        self.saver.delete_vacancy(self.test_vacancy)
        loaded_data = self.saver._JSONSaver__load_data()
        assert len(loaded_data) == 0
