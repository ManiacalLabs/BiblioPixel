from . base import TypesBaseTest


class DirectionTest(TypesBaseTest):
    def test_some(self):
        def test(name, expected):
            actual = self.make('direction', name)['direction']
            self.assertEqual(actual, expected)

        test('up', (0, -1))
        test('r', (1, 0))
        test((-1, 0), (-1, 0))
        test([0, 1], (0, 1))

        with self.assertRaises(ValueError):
            self.make('direction', 'sideways')

        with self.assertRaises(ValueError):
            self.make('direction', None)

        with self.assertRaises(ValueError):
            self.make('direction', (-1, -1))
