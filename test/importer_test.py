import unittest

from bibliopixel.util import importer

import_path = importer.import_path


class ImporterTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            import_path('')

    def test_single(self):
        import_path('math')
        import_path('bibliopixel')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            import_path('DOESNT_EXIST')

    def test_double(self):
        import_path('math.log')
        import_path('bibliopixel.util')

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            import_path('math12.log')

        with self.assertRaises(ImportError):
            import_path('math.log12')

        with self.assertRaises(ImportError):
            import_path('bibliopixel.log12')

    def test_longer(self):
        self.assertEqual(import_path('bibliopixel.util.importer'), importer)
        self.assertEqual(import_path('bibliopixel.util.importer.import_path'),
                         import_path)
