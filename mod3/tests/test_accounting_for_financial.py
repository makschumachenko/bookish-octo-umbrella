import unittest
from app import app
from collections import defaultdict


class TestFinanceApp(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        # Создаем и заполняем storage изначальными данными
        cls.storage = defaultdict(lambda: defaultdict(int))
        cls.storage[2022] = {1: 100, 2: 200, 3: 300}
        cls.storage[2023] = {1: 150, 2: 250, 3: 350}

    def test_add_expense_valid_date(self):
        tester = app.test_client(self)
        response = tester.get('/add/20240115/50')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Расход успешно добавлен".encode("utf-8"), response.data)

    def test_calculate_year(self):
        tester = app.test_client(self)
        response = tester.get('/calculate/2022')
        self.assertEqual(response.status_code, 200)
        self.assertIn('"total_expense": 600'.encode("utf-8"), response.data)

    def test_calculate_month(self):
        tester = app.test_client(self)
        response = tester.get('/calculate/2022/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn('"total_expense": 300'.encode("utf-8"), response.data)

    def test_add_expense_invalid_date(self):
        tester = app.test_client(self)
        response = tester.get('/add/20240132/50')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format".encode("utf-8"), response.data)

    def test_calculate_year_no_data(self):
        tester = app.test_client(self)
        response = tester.get('/calculate/2024')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Нет данных для выбранного года".encode("utf-8"), response.data)

    def test_calculate_month_no_data(self):
        tester = app.test_client(self)
        response = tester.get('/calculate/2022/4')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Нет данных для выбранного месяца и года".encode("utf-8"), response.data)


if __name__ == '__main__':
    unittest.main()
