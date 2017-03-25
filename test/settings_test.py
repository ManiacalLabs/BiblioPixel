import unittest
from bibliopixel.project.settings_file import get_setting


class SettingTest(unittest.TestCase):
    def test_all(self):
        section = {
            'a': {'foo': 1, 'bar': 2},
            'b': {'extends': 'a', 'bar': 3},
            'c': {'extends': 'b', 'bar': 4, 'foo': 2, 'baz': 7},
        }

        self.assertEqual(get_setting(section, 'a'), {'foo': 1, 'bar': 2})
        self.assertEqual(get_setting(section, 'b'), {'foo': 1, 'bar': 3})
        self.assertEqual(get_setting(section, 'c'),
                         {'foo': 2, 'bar': 4, 'baz': 7})
