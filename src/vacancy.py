from typing import Union

class Vacancy:
    """Класс для работы с вакансиями."""
    __slots__ = ('__title', '__url', '__salary_from', '__salary_to', '__description')

    def __init__(self, title: str, url: str, salary_from: Union[int, None] = None, salary_to: Union[int, None] = None, description: Union[str, None] = None):
        """Инициализирует объект вакансии."""
        self.__title = title
        self.__url = url
        self.__salary_from = salary_from if salary_from is not None else 0
        self.__salary_to = salary_to if salary_to is not None else 0
        self.__description = description
        self.__validate_data()

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def salary_from(self):
        return self.__salary_from

    @property
    def salary_to(self):
        return self.__salary_to

    @property
    def description(self):
        return self.__description

    def __lt__(self, other):
        return self.__salary_from < other.__salary_from

    def __gt__(self, other):
        return self.__salary_from > other.__salary_from

    def __eq__(self, other):
        return self.__salary_from == other.__salary_from

    def __validate_data(self):
        if self.__salary_from is None:
            self.__salary_from = 0

    def __str__(self):
        return f"Вакансия: {self.__title}\nURL: {self.__url}\nЗарплата от: {self.__salary_from}\nЗарплата до: {self.__salary_to}\nОписание: {self.__description}\n"
