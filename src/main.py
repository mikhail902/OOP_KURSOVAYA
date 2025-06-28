import re
from typing import List

from api_connectors import APIConnector, HHruConnector
from data_savers import DataSaver, JSONSaver
from vacancy import Vacancy


def interact_with_user(json_saver: JSONSaver, hh_connector: HHruConnector):
    """Функция для взаимодействия с пользователем через консоль."""

    def get_vacancies_from_api(query: str) -> List[Vacancy]:
        """Получает вакансии с API, преобразует в объекты Vacancy и возвращает список."""
        vacancies_data = hh_connector.get_vacancies(query)
        new_vacancies = []

        for data in vacancies_data:
            salary = data.get("salary") or {"from": None, "to": None}
            vacancy = Vacancy(
                title=data["name"],
                url=data["alternate_url"],
                salary_from=salary["from"],
                salary_to=salary["to"],
                description=data.get("snippet", {}).get("requirement"),
            )
            new_vacancies.append(vacancy)

        return new_vacancies

    def print_vacancies(vacancies: List[Vacancy]):
        """Выводит список вакансий на экран."""
        if not vacancies:
            print("Нет вакансий для отображения.")
            return

        for vacancy in vacancies:
            print(vacancy)

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Найти вакансии по ключевому слову в описании")
        print("4. Вывести все сохраненные вакансии")
        print("5. Удалить вакансию")
        print("6. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            query = input("Введите поисковый запрос для вакансий на hh.ru: ").strip()
            new_vacancies = get_vacancies_from_api(query)

            existing_urls = {v.url for v in json_saver.get_vacancies({})}
            unique_vacancies = [v for v in new_vacancies if v.url not in existing_urls]

            for vacancy in unique_vacancies:
                json_saver.add_vacancy(vacancy)
                print(f"Добавлена: {vacancy}")

            print(f"\nДобавлено {len(unique_vacancies)} новых вакансий.")

        elif choice == "2":
            try:
                n = int(input("Введите количество вакансий для вывода: "))
                all_vacancies = json_saver.get_vacancies({})
                sorted_vacancies = sorted(all_vacancies, reverse=True)[:n]
                print_vacancies(sorted_vacancies)
            except ValueError:
                print("Ошибка: введите число!")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ").strip()
            all_vacancies = json_saver.get_vacancies({})
            filtered = [
                v
                for v in all_vacancies
                if v.description and re.search(keyword, v.description, re.IGNORECASE)
            ]
            print_vacancies(filtered)

        elif choice == "4":
            print_vacancies(json_saver.get_vacancies({}))

        elif choice == "5":
            url = input("Введите URL вакансии для удаления: ").strip()
            if json_saver.delete_vacancy(Vacancy("", url)):
                print("Вакансия удалена.")
            else:
                print("Вакансия не найдена.")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    json_saver = JSONSaver()
    hh_connector = HHruConnector()
    interact_with_user(json_saver, hh_connector)
