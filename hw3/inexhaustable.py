import sys
import functools
import unittest


def inexhaustable(generator):

    """Return inexhaustable iterator for generator."""

    @functools.wraps(generator)
    def decorated(*args, **kwargs):
        class Iterable(object):
            def __iter__(self):
                return generator(*args, **kwargs)
        return Iterable()
    return decorated


class TestInexhaustable(unittest.TestCase):

    """Test @inexhaustable decorator."""

    def test_generic(self):
        @inexhaustable
        def foo():
            yield 1
            yield 2

        x = foo()
        self.assertListEqual(list(x), [1, 2])
        self.assertListEqual(list(x), [1, 2])


if __name__ == '__main__':
    unittest.main()
