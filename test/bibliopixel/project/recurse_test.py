import unittest
from bibliopixel.project import fields, recurse
from bibliopixel.util import colors


class Tester:
    @staticmethod
    def post_recursion(x):
        for k, v in x.items():
            if k != 'typename' and isinstance(v, str):
                x[k] = 'post-' + x[k]

    CHILDREN = 'foo',


class RecurseTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(recurse.recurse({}), {})

    def test_trivial(self):
        self.assertEqual(recurse.recurse({'a': {}}), {'a': {}})

    post_recursion = staticmethod(fields.default_converter)

    def test_simple(self):
        source = {'datatype': RecurseTest, 'foo': 'bar', 'color': 'red'}
        expected = {'datatype': RecurseTest, 'foo': 'bar', 'color': colors.Red}
        actual = recurse.recurse(source, post='post_recursion')
        self.assertEqual(expected, actual)

    def test_complex(self):
        source = {
            'typename': '%s.%s' % (Tester.__module__, Tester.__name__),
            'foo': {'datatype': RecurseTest, 'foo': 'bar', 'color': 'red'},
            'bing': 'bang',
        }
        expected = {
            'datatype': Tester,
            'foo': {'datatype': RecurseTest, 'foo': 'bar', 'color': colors.Red},
            'bing': 'post-bang',
        }
        actual = recurse.recurse(source, post='post_recursion')
        self.assertEqual(expected, actual)
