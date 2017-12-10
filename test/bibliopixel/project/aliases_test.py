import unittest
from bibliopixel.project import aliases, alias_lists, importer
from test.bibliopixel import patch


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(aliases.resolve(''), '')

    def test_resolve(self):
        self.assertEqual(
            aliases.resolve('off'), 'bibliopixel.animation.off.OffAnim')
        self.assertEquals(aliases.resolve('foo'), 'foo')

        with patch.patch(aliases.alias_lists, 'USER_ALIASES', {'foo': 'bar'}):
            self.assertEquals(aliases.resolve('foo'), 'bar')
            self.assertEquals(aliases.resolve('@foo.bing'), 'bar.bing')
            self.assertEquals(aliases.resolve('bar.bing.@foo'), 'bar.bing.bar')
            self.assertEquals(aliases.resolve('x@foo'), 'x@foo')

    def test_preserve_separators(self):
        s = '.asdfa./#fahdwrdr./#435'
        self.assertEqual(aliases.resolve(s), s)

    def test_marker(self):
        old_user = aliases.alias_lists.USER_ALIASES
        aliases.alias_lists.USER_ALIASES = {'foo': 'bar.com/a.html'}
        try:
            result = aliases.resolve('https://@foo#tag')
        finally:
            aliases.alias_lists.USER_ALIASES = old_user

        self.assertEqual(result, 'https://bar.com/a.html#tag')

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

    def test_additional_aliases(self):
        additional = {'foo': 'bar', 'remote': 'distance'}
        self.assertEqual(aliases.resolve('foo', additional), 'bar')
        self.assertEqual(aliases.resolve('remote', additional), 'distance')
