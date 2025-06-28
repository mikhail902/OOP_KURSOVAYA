import abc
import json
import uuid
from typing import Dict, List, Optional, Union

from vacancy import Vacancy


class DataSaver(abc.ABC):
    """Абстрактный класс для сохранения и загрузки вакансий из файла."""

    @abc.abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abc.abstractmethod
    def get_vacancies(
        self, criteria: Optional[Dict[str, Union[str, int, None]]] = None
    ) -> List[Vacancy]:
        pass

    @abc.abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass


class JSONSaver(DataSaver):
    """Класс для сохранения и загрузки вакансий в JSON-файл."""

    def __init__(
        self,
        filename: str = "C:/Users/Sator/PycharmProjects/OOP_KURSOVAYA/data/vacancies.json",
    ):
        self.filename = filename
        self.data = self.__load_data()

    def __load_data(self) -> List[Dict]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Ошибка загрузки файла {self.filename}: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке файла: {e}")
            return []

    def _validate_data_structure(self):
        """Проверяет структуру загруженных данных и исправляет при необходимости."""
        valid_data = []
        for item in self.data:
            if not isinstance(item, dict):
                continue

            required_fields = {
                "title",
                "url",
                "salary_from",
                "salary_to",
                "description",
            }
            if not all(field in item for field in required_fields):
                continue

            valid_data.append(
                {
                    "title": str(item["title"]),
                    "url": str(item["url"]),
                    "salary_from": (
                        item["salary_from"]
                        if isinstance(item["salary_from"], (int, float))
                        else None
                    ),
                    "salary_to": (
                        item["salary_to"]
                        if isinstance(item["salary_to"], (int, float))
                        else None
                    ),
                    "description": (
                        str(item["description"]) if item["description"] else None
                    ),
                    "id": str(item.get("id", uuid.uuid4().hex)),
                }
            )
        self.data = valid_data
        if len(valid_data) != len(self.data):
            self._save_data()

    def _save_data(self):
        """Сохраняет данные в файл с обработкой ошибок."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except (IOError, TypeError) as e:
            print(f"Ошибка сохранения данных: {e}")
            raise RuntimeError(f"Не удалось сохранить данные в файл: {e}")

    def _vacancy_to_dict(self, vacancy: Vacancy) -> Dict:
        """Конвертирует объект Vacancy в словарь для хранения."""
        return {
            "id": uuid.uuid4().hex,
            "title": vacancy.title,
            "url": vacancy.url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "description": vacancy.description,
        }

    def _dict_to_vacancy(self, data: Dict) -> Vacancy:
        """Создает объект Vacancy из словаря."""
        return Vacancy(
            title=data["title"],
            url=data["url"],
            salary_from=data["salary_from"],
            salary_to=data["salary_to"],
            description=data["description"],
        )

    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """Добавляет вакансию, если она не существует."""
        if not isinstance(vacancy, Vacancy):
            raise TypeError("Ожидается объект Vacancy")

        existing_urls = {v["url"] for v in self.data}
        existing_titles = {v["title"].lower() for v in self.data}

        if vacancy.url in existing_urls:
            print(f"Вакансия с URL {vacancy.url} уже существует")
            return False

        if vacancy.title.lower() in existing_titles:
            print(f"Вакансия с названием '{vacancy.title}' уже существует")
            return False

        self.data.append(self._vacancy_to_dict(vacancy))
        try:
            self._save_data()
            print(f"Добавлена вакансия: {vacancy.title}")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении вакансии: {e}")
            self.data.pop()
            return False

    def get_vacancies(
        self, criteria: Optional[Dict[str, Union[str, int, None]]] = None
    ) -> List[Vacancy]:
        """Возвращает вакансии, отфильтрованные по критериям."""
        if not criteria:
            return [self._dict_to_vacancy(v) for v in self.data]

        results = []
        for item in self.data:
            match = True
            for key, value in criteria.items():
                if value is None:
                    continue

                if key not in item or item[key] != value:
                    match = False
                    break

            if match:
                results.append(self._dict_to_vacancy(item))

        return results

    def delete_vacancy(self, vacancy: Vacancy) -> bool:
        """Удаляет вакансию по совпадению URL."""
        initial_count = len(self.data)
        self.data = [v for v in self.data if v["url"] != vacancy.url]

        if len(self.data) < initial_count:
            try:
                self._save_data()
                print(f"Удалена вакансия: {vacancy.title}")
                return True
            except Exception as e:
                print(f"Ошибка при удалении вакансии: {e}")
                return False

        print(f"Вакансия с URL {vacancy.url} не найдена")
        return False

    def __str__(self):
        return f"JSONSaver(file='{self.filename}', vacancies={len(self.data)})"
