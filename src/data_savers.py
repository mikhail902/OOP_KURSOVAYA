import abc
import json
from typing import List, Dict
from vacancy import Vacancy

class DataSaver(abc.ABC):
    """Абстрактный класс для сохранения и загрузки вакансий из файла."""
    @abc.abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abc.abstractmethod
    def get_vacancies(self, criteria: Dict) -> List[Vacancy]:
        pass

    @abc.abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass

class JSONSaver(DataSaver):
    """Класс для сохранения и загрузки вакансий в JSON-файл."""

    def __init__(self, filename: str = "C:/Users/Sator/PycharmProjects/OOP_KURSOVAYA/data/vacancies.json"):
        self.filename = filename
        self.data = self.__load_data()

    def __load_data(self) -> List[Dict]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка: Файл JSON поврежден. Возвращен пустой список.")
            return []

    def __save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        """
        Добавляет вакансию в JSON-файл, предотвращая дублирование.
        """
        vacancy_data = {
            'title': vacancy.title,
            'url': vacancy.url,
            'salary_from': vacancy.salary_from,
            'salary_to': vacancy.salary_to,
            'description': vacancy.description
        }
        if not self.__is_duplicate(vacancy):
            self.data.append(vacancy_data)
            self.__save_data()
            print(f"Вакансия {vacancy.title} добавлена.")
        else:
            print(f"Вакансия {vacancy.title} уже существует.")

    def __is_duplicate(self, vacancy: Vacancy) -> bool:
        """
        Проверяет, является ли вакансия дубликатом (по URL).
        """
        for item in self.data:
            if item.get('url') == vacancy.url:
                return True
        return False

    def get_vacancies(self, criteria: Dict) -> List[Vacancy]:
        results = []
        for vacancy_data in self.data:
            match = True
            for key, value in criteria.items():
                if value is not None and vacancy_data.get(key) != value:
                    match = False
                    break
            if match:
                vacancy = Vacancy(
                    vacancy_data['title'],
                    vacancy_data['url'],
                    vacancy_data['salary_from'],
                    vacancy_data['salary_to'],
                    vacancy_data['description']
                )
                results.append(vacancy)
        return results

    def delete_vacancy(self, vacancy: Vacancy):
        initial_len = len(self.data)
        self.data = [v for v in self.data if v['url'] != vacancy.url]
        if len(self.data) < initial_len:
            self.__save_data()
            print(f"Вакансия с URL {vacancy.url} удалена.")
        else:
            print(f"Вакансия с URL {vacancy.url} не найдена.")
