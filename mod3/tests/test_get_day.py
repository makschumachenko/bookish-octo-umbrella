import unittest
from app import app
from freezegun import freeze_time
from get_day import get_day_of_week_name

class TestHelloWorld(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    @freeze_time("2024-04-08")
    def test_can_get_correct_username_with_weekdate(self):
        with app.test_client() as client:
            response = client.get('/hello-world/John')
            self.assertIn('Хорошего понедельника'.encode('utf-8'), response.data)

    def test_day_of_week_name_correctness(self):
        self.assertEqual(get_day_of_week_name(0), "Хорошего понедельника")
        self.assertEqual(get_day_of_week_name(1), "Хорошего вторника")
        self.assertEqual(get_day_of_week_name(2), "Хорошей среды")
        self.assertEqual(get_day_of_week_name(3), "Хорошего четверга")
        self.assertEqual(get_day_of_week_name(4), "Хорошей пятницы")
        self.assertEqual(get_day_of_week_name(5), "Хорошей субботы")
        self.assertEqual(get_day_of_week_name(6), "Хорошего воскресенье")


if __name__ == '__main__':
    unittest.main()
