import re
from typing import List, Dict
from api_connectors import HHruConnector, APIConnector
from vacancy import Vacancy
from data_savers import JSONSaver, DataSaver

def interact_with_user(json_saver: JSONSaver, hh_connector: HHruConnector):
    """Функция для взаимодействия с пользователем через консоль."""

    def get_vacancies_from_api(query: str):
        """Вспомогательная функция для получения вакансий с API и сохранения."""
        vacancies_data = hh_connector.get_vacancies(query)
        for data in vacancies_data:
            salary = data['salary'] if data['salary'] else {'from': None, 'to': None}
            vacancy = Vacancy(
                data['name'],
                data['alternate_url'],
                salary_from=salary['from'],
                salary_to=salary['to'],
                description=data['snippet']['requirement'] if data['snippet'] else None
            )
            json_saver.add_vacancy(vacancy)
            print(vacancy)

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
            get_vacancies_from_api(query)

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
                    if vacancy.description and re.search(keyword, vacancy.description, re.IGNORECASE):
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

if __name__ == '__main__':
    json_saver = JSONSaver()
    hh_connector = HHruConnector()
    interact_with_user(json_saver, hh_connector)
