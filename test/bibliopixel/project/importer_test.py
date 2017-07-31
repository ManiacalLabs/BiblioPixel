import unittest

from bibliopixel.project.importer import import_symbol, make_object
from bibliopixel.project import importer


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
        self.assertEqual(
            import_symbol('bibliopixel.project.importer'), importer)
        self.assertEqual(
            import_symbol('bibliopixel.project.importer.import_symbol'),
            import_symbol)

    def test_make_object(self):
        td = make_object(5, 23, typename='datetime.timedelta', milliseconds=35)
        import datetime
        self.assertEqual(td, datetime.timedelta(5, 23, milliseconds=35))

    def test_aliasing(self):
        import_symbol('bibliopixel.drivers.SimPixel.SimPixel')

    def test_exception_unknown(self):
        with self.assertRaises(ImportError) as cm:
            import_symbol('nonexistent')
        e = str(cm.exception)
        self.assertFalse('pip install' in e)
        self.assertTrue('No module named \'nonexistent\'' in e)

    def test_exception_known(self):
        try:
            # Patch in a known, "fake" module.
            importer.INSTALL_NAMES['nonexistent'] = 'pynone'
            with self.assertRaises(ImportError) as cm:
                import_symbol('nonexistent')
            e = str(cm.exception)
            self.assertTrue('pip install pynone' in e)
            self.assertTrue('No module named \'nonexistent\'' in e)

        finally:
            importer.INSTALL_NAMES.pop('nonexistent')
