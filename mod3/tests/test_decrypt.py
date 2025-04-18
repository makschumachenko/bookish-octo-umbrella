import unittest
from app import app

class TestDecrypt(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_single_dot(self):
        response = self.client.post('/decrypt', data='.')
        self.assertEqual(response.data.decode('utf-8'), "")

    def test_multiple_dots(self):
        response = self.client.post('/decrypt', data='1.......................')
        self.assertEqual(response.data.decode('utf-8'), "")

    def test_no_dots(self):
        response = self.client.post('/decrypt', data='абра-кадабра.')
        self.assertEqual(response.data.decode('utf-8'), "абра-кадабра")

    def test_one_dot(self):
        response = self.client.post('/decrypt', data='абра.-кадабра')
        self.assertEqual(response.data.decode('utf-8'), "абра-кадабра")

    def test_two_dots(self):
        response = self.client.post('/decrypt', data='абраа..-кадабра')
        self.assertEqual(response.data.decode('utf-8'), "абра-кадабра")

    def test_three_dots(self):
        response = self.client.post('/decrypt', data='абра--..кадабра')
        self.assertEqual(response.data.decode('utf-8'), "абра-кадабра")

    def test_with_letter(self):
        response = self.client.post('/decrypt', data='абр......a.')
        self.assertEqual(response.data.decode('utf-8'), "a")

    def test_numbers(self):
        response = self.client.post('/decrypt', data='1..2.3')
        self.assertEqual(response.data.decode('utf-8'), "23")

    def test_decrypt_empty_string(self):
        response = self.client.post('/decrypt', data='.')
        self.assertEqual(response.data.decode('utf-8'), "")

    def test_decrypt_long_string(self):
        response = self.client.post('/decrypt', data='1.......................')
        self.assertEqual(response.data.decode('utf-8'), "")


if __name__ == '__main__':
    unittest.main()