import unittest
from app import app


# task3 Для каждого поля и валидатора в endpoint /registration напишите юнит-тест, который проверит корректность
# работы валидатора.
class TestRegistrationForm(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_registration_form_valid(self):
        data = {
            'email': 'test@kuga.com',
            'phone': 1234567890,
            'name': 'andrey kag',
            'address': '123 Test St',
            'index': 12345
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)

    def test_registration_form_missing_fields(self):
        data = {
            'email': 'test@example.com',
            'phone': 1234567890,
            # Missing 'name', 'address', and 'index'
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)

    def test_registration_form_invalid_phone(self):
        data = {
            'email': 'test@example.com',
            'phone': 123,
            'name': 'Test User',
            'address': '123 Test St',
            'index': 12345
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)

    def test_registration_form_invalid_index(self):
        data = {
            'email': 'test@example.com',
            'phone': 1234567890,
            'name': 'Test User',
            'address': '123 Test St',
            'index': 'abc'
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
