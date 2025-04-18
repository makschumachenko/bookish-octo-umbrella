import unittest
import datetime


class Person:
    def __init__(self, name, year_of_birth, address=''):
        self.name = name
        self.yob = year_of_birth
        self.address = address

    def get_age(self):
        now = datetime.datetime.now()
        return now.year - self.yob

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address if self.address != '' else None

    def is_homeless(self):
        return self.address == ''


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person_with_address = Person("Andrey", 1990, "yekaterinburg")
        self.person_without_address = Person("Alice", 1985)

    def test_get_age(self):
        current_year = datetime.datetime.now().year
        self.assertEqual(self.person_with_address.get_age(), current_year - 1990)
        self.assertEqual(self.person_without_address.get_age(), current_year - 1985)

    def test_get_name(self):
        self.assertEqual(self.person_with_address.get_name(), "Andrey")
        self.assertEqual(self.person_without_address.get_name(), "Alice")

    def test_set_name(self):
        self.person_with_address.set_name("Anton")
        self.assertEqual(self.person_with_address.get_name(), "Anton")

    def test_set_address(self):
        self.person_without_address.set_address("moscow")
        self.assertEqual(self.person_without_address.get_address(), "moscow")

    def test_get_address(self):
        self.assertEqual(self.person_with_address.get_address(), "yekaterinburg")
        self.assertIsNone(self.person_without_address.get_address(), "")

    def test_is_homeless(self):
        self.assertFalse(self.person_with_address.is_homeless())
        self.assertTrue(self.person_without_address.is_homeless())

if __name__ == '__main__':
    unittest.main()
