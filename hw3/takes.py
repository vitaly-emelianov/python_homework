import sys
import functools
import unittest


def takes(*args_types):

    """Return decorator to function, which checks types of arguments to be corresponding."""

    def decorator(func):
        @functools.wraps(func)
        def decorated(*args):
            for arg_type, arg in zip(args_types, args):
                if type(arg) != arg_type:
                    raise TypeError
            return func(*args)
        return decorated
    return decorator


class TestTakesDecorator(unittest.TestCase):

    """Test @takes(*args_types) decorator."""

    def test_generic(self):

        @takes(str, float)
        def foo(name, height):
            return (name, height)

        # test if raises TypeError
        with self.assertRaises(TypeError):
            foo(12, 3.0)

        # test if returns what it should return
        self.assertEqual(('name', 3.0), foo('name', 3.0))


if __name__ == '__main__':
    unittest.main()
