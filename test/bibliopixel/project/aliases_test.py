import unittest
from bibliopixel.project import aliases, alias_lists, importer


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(aliases.resolve({}), {})

    def test_simple(self):
        d = {'typename': 'bibliopixel.layout.circle.Circle'}
        self.assertEqual(aliases.resolve(d), d)

    def test_resolve(self):
        d = {'typename': 'bibliopixel.layout.circle.Circle'}
        self.assertEqual(aliases.resolve('circle'), d)
        self.assertEqual(aliases.resolve({'typename': 'circle'}), d)

        d['foo'] = 'bar'
        self.assertEqual(
            aliases.resolve({'typename': 'circle', 'foo': 'bar'}), d)

    def test_existence(self):
        failed = []
        for cl in alias_lists.BUILTIN_ALIASES.values():
            try:
                importer.import_symbol(cl)
            except:
                failed.append(cl)

        if failed:
            print('Failed', *failed, sep='\n')
        self.assertFalse(failed)
