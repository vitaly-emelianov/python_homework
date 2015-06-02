import sys
import unittest


class AssertRaises(object):

    """AssertRaises context manager."""

    def __init__(self, exception_type):
        self.exception_type = exception_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (exc_type != self.exception_type):
            raise AssertionError
        else:
            return True


class TestAssertRaises(unittest.TestCase):

    """Test AssertRaises() context manager."""

    def test_generic(self):

        def foo(number):
            if number > 10:
                raise ValueError
            else:
                return number

        # test if raises AssertionError
        with self.assertRaises(AssertionError):
            with AssertRaises(TypeError):
                raise ValueError

        # test if not raises any error
        try:
            with AssertRaises(ValueError):
                foo(100)
        except Exception:
            self.fail("foo() raised exception unexpectedly.")


if __name__ == '__main__':
    unittest.main()
