import unittest
from mod5.task3.block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_error_ignored(self):
        err_types = {ZeroDivisionError}
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)

    def test_error_raised(self):
        err_types = {TypeError}
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors(err_types):
                a = 1 / 0


    def test_inner_block_error_raised_outer_ignored(self):
        outer_err_types = {TypeError}
        inner_err_types = {ZeroDivisionError}
        with BlockErrors(outer_err_types):
            with self.assertRaises(ZeroDivisionError):
                with BlockErrors(inner_err_types):
                    a = 1 / '0'

    def test_child_errors_ignored(self):
        err_types = {ArithmeticError}  # ArithmeticError является базовым классом для ZeroDivisionError
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
