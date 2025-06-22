import abc
import json
import re
from typing import Dict, List, Union

import requests


class APIConnector(abc.ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abc.abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает вакансии из API."""
        pass


class HHruConnector(APIConnector):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        """Инициализирует объект HHruConnector."""
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает вакансии с hh.ru."""
        try:
            params = {"text": query, "area": 113, "per_page": 100}  # Parameters
            response = self.__send_request(self.__base_url, params)

            data = response.json()
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API hh.ru: {e}")
            return []

    def __send_request(self, url: str, params: Dict) -> requests.Response:
        """Отправляет GET-запрос к API и обрабатывает ответ."""
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response


class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = ("title", "url", "salary_from", "salary_to", "description")

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Union[int, None] = None,
        salary_to: Union[int, None] = None,
        description: Union[str, None] = None,
    ):
        """Инициализирует объект вакансии."""
        self.title = title
        self.url = url
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.description = description
        self.__validate_data()

    def __lt__(self, other):
        """Сравнивает вакансии по зарплате (меньше)."""
        return self.salary_from < other.salary_from

    def __gt__(self, other):
        """Сравнивает вакансии по зарплате (больше)."""
        return self.salary_from > other.salary_from

    def __eq__(self, other):
        """Сравнивает вакансии по зарплате (равно)."""
        return self.salary_from == other.salary_from

    def __validate_data(self):
        """Валидирует данные вакансии. Если зарплата не указана, устанавливает значение 0."""
        if self.salary_from is None:
            self.salary_from = 0

    def __str__(self):
        return f"Вакансия: {self.title}\nURL: {self.url}\nЗарплата от: {self.salary_from}\nЗарплата до: {self.salary_to}\nОписание: {self.description}\n"


class DataSaver(abc.ABC):
    """Абстрактный класс для сохранения и загрузки вакансий из файла."""

    @abc.abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """Добавляет вакансию в файл."""
        pass

    @abc.abstractmethod
    def get_vacancies(self, criteria: Dict) -> List[Vacancy]:
        """Получает вакансии из файла по критериям."""
        pass

    @abc.abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        """Удаляет информацию о вакансии из файла."""
        pass


class JSONSaver(DataSaver):
    """Класс для сохранения и загрузки вакансий в JSON-файл."""

    def __init__(
        self,
        filename: str = "C:/Users/Sator/PycharmProjects/OOP_KURSOVAYA/data/vacancies.json",
    ):
        """Инициализирует объект JSONSaver."""
        self.filename = filename
        self.data = self.__load_data()

    def __load_data(self) -> List[Dict]:
        """Загружает данные из JSON-файла. Создает пустой файл, если он не существует."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка: Файл JSON поврежден. Возвращен пустой список.")
            return []

    def __save_data(self):
        """Сохраняет данные в JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        """Добавляет вакансию в JSON-файл."""
        vacancy_data = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "description": vacancy.description,
        }
        self.data.append(vacancy_data)
        self.__save_data()

    def get_vacancies(self, criteria: Dict) -> List[Vacancy]:
        """Получает вакансии из JSON-файла по критериям."""
        results = []
        for vacancy_data in self.data:
            match = True
            for key, value in criteria.items():
                if value is not None and vacancy_data.get(key) != value:
                    match = False
                    break
            if match:
                vacancy = Vacancy(
                    vacancy_data["title"],
                    vacancy_data["url"],
                    vacancy_data["salary_from"],
                    vacancy_data["salary_to"],
                    vacancy_data["description"],
                )
                results.append(vacancy)
        return results

    def delete_vacancy(self, vacancy: Vacancy):
        """Удаляет информацию о вакансии из JSON-файла. Сравнивает по URL."""
        initial_len = len(self.data)
        self.data = [v for v in self.data if v["url"] != vacancy.url]
        if len(self.data) < initial_len:
            self.__save_data()
            print(f"Вакансия с URL {vacancy.url} удалена.")
        else:
            print(f"Вакансия с URL {vacancy.url} не найдена.")


def interact_with_user(json_saver: JSONSaver, hh_connector: HHruConnector):
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Найти вакансии по ключевому слову в описании")
        print("4. Вывести все сохраненные вакансии")
        print("5. Удалить вакансию")
        print("6. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            query = input("Введите поисковый запрос для вакансий на hh.ru: ")
            vacancies_data = hh_connector.get_vacancies(query)
            for data in vacancies_data:
                salary = (
                    data["salary"] if data["salary"] else {"from": None, "to": None}
                )
                vacancy = Vacancy(
                    data["name"],
                    data["alternate_url"],
                    salary_from=salary["from"],
                    salary_to=salary["to"],
                    description=(
                        data["snippet"]["requirement"] if data["snippet"] else None
                    ),
                )
                json_saver.add_vacancy(vacancy)
                print(vacancy)

        elif choice == "2":
            n = int(input("Введите количество вакансий для вывода: "))
            all_vacancies = json_saver.get_vacancies({})
            if all_vacancies:
                sorted_vacancies = sorted(all_vacancies, reverse=True)
                for i in range(min(n, len(sorted_vacancies))):
                    print(sorted_vacancies[i])
            else:
                print("Нет сохраненных вакансий.")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании вакансий: ")
            all_vacancies = json_saver.get_vacancies({})
            if all_vacancies:
                for vacancy in all_vacancies:
                    if vacancy.description and re.search(
                        keyword, vacancy.description, re.IGNORECASE
                    ):
                        print(vacancy)
            else:
                print("Нет сохраненных вакансий.")

        elif choice == "4":
            all_vacancies = json_saver.get_vacancies({})
            if all_vacancies:
                for vacancy in all_vacancies:
                    print(vacancy)
            else:
                print("Нет сохраненных вакансий.")

        elif choice == "5":
            url_to_delete = input("Введите URL вакансии для удаления: ")
            vacancy_to_delete = Vacancy("", url_to_delete)
            json_saver.delete_vacancy(vacancy_to_delete)

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    json_saver = JSONSaver()
    hh_connector = HHruConnector()
    interact_with_user(json_saver, hh_connector)
