import time, unittest
from bibliopixel.builder.builder import Builder
from bibliopixel.util import data_file


class BuilderTest(unittest.TestCase):
    def test_simple(self):
        b = Builder(driver='dummy')

        self.assertFalse(b.is_running)
        b.start(True)
        self.assertTrue(b.is_running)
        b.stop()

    def test_merging(self):
        b = Builder(driver='.dummy') + {'animation': '.tests.PixelTester'}
        b.desc.shape = [12, 16]
        b.start(True)
        actual = b.desc.as_dict()
        b.stop()
        expected = {
            'animation': {'typename': '.tests.PixelTester'},
            'driver': {'typename': '.dummy'},
            'run': {'threaded': True},
            'shape': [12, 16]}
        self.assertEqual(actual, expected)
