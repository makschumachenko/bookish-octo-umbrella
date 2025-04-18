import unittest
from collections import defaultdict
from app import app

class TestExpenses(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.fill_storage()

    def tearDown(self):
        pass

    def fill_storage(self):
        # Заполнение storage данными для тестирования
        self.storage = defaultdict(lambda: defaultdict(int))
        self.storage[2024][1] = 100  # Предположим, что в январе 2024 был расход 100
        self.storage[2024][2] = 200  # Предположим, что в феврале 2024 был расход 200

    def test_add_expense(self):
        # Тестирование добавления расхода
        response = self.app.get('/add/20240101/100')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Расход успешно добавлен".encode("utf-8"), response.data)

    def test_calculate_year(self):
        # Тестирование расчета расходов за год
        response = self.app.get('/calculate/2024')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"total_expense":100', response.data)

    def test_calculate_month(self):
        # Тестирование расчета расходов за месяц
        response = self.app.get('/calculate/2024/01')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"total_expense":100', response.data)

    def test_invalid_date_format(self):
        # Тестирование неправильного формата даты
        response = self.app.get('/add/20241345/100')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format".encode("utf-8"), response.data)

    def test_no_data_for_year(self):
        # Тестирование запроса данных для несуществующего года
        response = self.app.get('/calculate/2023')
        self.assertEqual(response.status_code, 404)
        error_message = response.json['error']
        self.assertEqual(error_message, "Нет данных для выбранного года")

    def test_no_data_for_month(self):
        # Тестирование запроса данных для несуществующего месяца и года
        response = self.app.get('/calculate/2024/02')
        self.assertEqual(response.status_code, 404)
        error_message = response.json['error']
        self.assertEqual(error_message, "Нет данных для выбранного месяца и года")


if __name__ == '__main__':
    unittest.main()
