import unittest
from unittest.mock import patch
from bibliopixel.project import load


class LoadTest(unittest.TestCase):
    @patch('platform.system', autospec=True)
    def test_split_path(self, platform):
        platform.return_value = 'Darwin'
        to_split = 'abc;def:ghi;jkl:mn'
        actual = load._split_path(to_split)
        expected = ['abc', 'def', 'ghi', 'jkl', 'mn']
        self.assertEqual(actual, expected)

    @patch('platform.system', autospec=True)
    def test_split_path(self, platform):
        platform.return_value = 'Windows'
        to_split = 'abc;def:ghi;jkl:mn'
        actual = load._split_path(to_split)
        expected = ['abc', 'def:ghi', 'jkl:mn']
        self.assertEqual(actual, expected)
