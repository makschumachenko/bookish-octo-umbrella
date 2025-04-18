import unittest
from mod5.task2.code_runner import app


class TestCodeRunner(unittest.TestCase):
    valid_code_and_timeout = {
        'code': 'import time; time.sleep(10); print(1)',
        'timeout': '20'
    }

    less_time = '1'

    invalid_code = 'some_boolshit'

    damaged_code = 'from subprocess import run; run([\'./kill_the_system.sh\'])'

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестирования
        self.app = app.test_client()
        self.base_url = '/codeRuner'
        self.data = self.valid_code_and_timeout.copy()

    def test_valid_code_an_time(self):
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 200)

    def test_timout_less_then_running_time(self):
        self.data['timeout'] = self.less_time
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue('превышен лимит времени' in response.data.decode())

    def test_incorrect_form_data(self):
        self.data['code'] = self.invalid_code
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Ошибка при попытке запуска кода' in response.data.decode())

    def test_running_damaged_code(self):
        self.data['code'] = self.damaged_code
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Resource temporarily unavailable' in response.data.decode())

