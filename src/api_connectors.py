import abc
import requests
from typing import List, Dict

class APIConnector(abc.ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abc.abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает вакансии из API."""
        pass

class HHruConnector(APIConnector):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает вакансии с hh.ru."""
        try:
            params = {'text': query, 'area': 113, 'per_page': 100}  # area: 113 - Россия
            response = self.__send_request(self.__base_url, params)
            data = response.json()
            return data.get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API hh.ru: {e}")
            return []

    def __send_request(self, url: str, params: Dict) -> requests.Response:
        """Отправляет GET-запрос к API и обрабатывает ответ."""
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response
