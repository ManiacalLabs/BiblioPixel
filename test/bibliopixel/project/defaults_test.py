import unittest

from bibliopixel.project import defaults


class DefaultsTest(unittest.TestCase):
    def run_test(self, expected, *sections):
        actual = defaults._sections_to_assignments(sections)
        self.assertEqual(expected, actual)

    def run_failure(self, *sections, exception=ValueError):
        with self.assertRaises(exception):
            defaults._sections_to_assignments(sections)

    def test_empty(self):
        self.run_failure()

    def test_json(self):
        self.run_test({"shape": 5}, '{"shape": 5}')
        self.run_failure('{"shapeX": 5}')

    def test_sections1(self):
        self.run_test({"shape": 5}, 'shape=5')
        self.run_failure('shapeX=5')

    def test_sections2(self):
        data = 'animation={"typename": "feedback", "master": 2}'
        expected = {"animation": {"typename": "feedback", "master": 2}}
        self.run_test(expected, data)
        self.run_test(
            expected, 'animation.typename=feedback', 'animation.master=2')
