import unittest

from bibliopixel.util import importer

import_symbol = importer.import_symbol


class ImporterTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            import_symbol('')

    def test_single(self):
        import_symbol('math')
        import_symbol('bibliopixel')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            import_symbol('DOESNT_EXIST')

    def test_double(self):
        import_symbol('math.log')
        import_symbol('bibliopixel.util')

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            import_symbol('math12.log')

        with self.assertRaises(ImportError):
            import_symbol('math.log12')

        with self.assertRaises(ImportError):
            import_symbol('bibliopixel.log12')

    def test_longer(self):
        self.assertEqual(import_symbol('bibliopixel.util.importer'), importer)
        self.assertEqual(import_symbol('bibliopixel.util.importer.import_symbol'),
                         import_symbol)

    def test_make_object(self):
        td = importer.make_object(5, 23, typename='datetime.timedelta',
                                  milliseconds=235)
        import datetime
        self.assertEqual(td, datetime.timedelta(5, 23, milliseconds=235))
