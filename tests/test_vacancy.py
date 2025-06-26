import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def test_init(self):
        """Проверяет инициализацию объекта Vacancy."""
        vacancy = Vacancy(
            title="Test Title",
            url="http://test.com",
            salary_from=100,
            salary_to=200,
            description="Test Description",
        )
        self.assertEqual(vacancy.title, "Test Title")
        self.assertEqual(vacancy.url, "http://test.com")
        self.assertEqual(vacancy.salary_from, 100)
        self.assertEqual(vacancy.salary_to, 200)
        self.assertEqual(vacancy.description, "Test Description")

    def test_init_with_none_salary(self):
        """Проверяет инициализацию объекта Vacancy с None в качестве зарплаты."""
        vacancy = Vacancy(
            title="Test Title",
            url="http://test.com",
            salary_from=None,
            salary_to=None,
            description="Test Description",
        )
        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)

    def test_init_without_description(self):
        """Проверяет инициализацию объекта Vacancy без описания."""
        vacancy = Vacancy(
            title="Test Title", url="http://test.com", salary_from=100, salary_to=200
        )
        self.assertEqual(vacancy.description, None)

    def test_lt(self):
        """Проверяет оператор < (меньше чем)."""
        vacancy1 = Vacancy(
            title="Test Title", url="http://test.com", salary_from=100, salary_to=200
        )
        vacancy2 = Vacancy(
            title="Another Title",
            url="http://another.com",
            salary_from=200,
            salary_to=300,
        )
        self.assertTrue(vacancy1 < vacancy2)
        self.assertFalse(vacancy2 < vacancy1)

    def test_gt(self):
        """Проверяет оператор > (больше чем)."""
        vacancy1 = Vacancy(
            title="Test Title", url="http://test.com", salary_from=100, salary_to=200
        )
        vacancy2 = Vacancy(
            title="Another Title",
            url="http://another.com",
            salary_from=200,
            salary_to=300,
        )
        self.assertTrue(vacancy2 > vacancy1)
        self.assertFalse(vacancy1 > vacancy2)

    def test_eq(self):
        """Проверяет оператор == (равно)."""
        vacancy1 = Vacancy(
            title="Test Title", url="http://test.com", salary_from=100, salary_to=200
        )
        vacancy2 = Vacancy(
            title="Another Title",
            url="http://another.com",
            salary_from=100,
            salary_to=300,
        )
        vacancy3 = Vacancy(
            title="Different Title",
            url="http://different.com",
            salary_from=200,
            salary_to=300,
        )
        self.assertTrue(vacancy1 == vacancy2)
        self.assertFalse(vacancy1 == vacancy3)

    def test_validate_data(self):
        """Проверяет метод валидации данных."""
        vacancy = Vacancy(
            title="Test Title",
            url="http://test.com",
            salary_from=None,
            salary_to=200,
            description="Test Description",
        )
        self.assertEqual(vacancy.salary_from, 0)

    def test_str(self):
        """Проверяет строковое представление объекта."""
        vacancy = Vacancy(
            title="Test Title",
            url="http://test.com",
            salary_from=100,
            salary_to=200,
            description="Test Description",
        )
        expected_string = "Вакансия: Test Title\nURL: http://test.com\nЗарплата от: 100\nЗарплата до: 200\nОписание: Test Description\n"
        self.assertEqual(str(vacancy), expected_string)


if __name__ == "__main__":
    unittest.main()
