import collections, unittest
from bibliopixel.util.colors import palette, palettes
from bibliopixel.colors import COLORS
from bibliopixel.util.colors.legacy_palette import pop_legacy_palette


class LegacyPaletteTest(unittest.TestCase):
    def test_simple(self):
        kwds = {}
        pal = pop_legacy_palette(kwds)
        self.assertFalse(kwds)
        self.assertEqual(pal, palettes.get())

    def test_palette(self):
        pal = 'wombat'
        for k in 'palette', 'colors':
            kwds = {k: pal, 'other': 'stuff'}
            self.assertIs(pal, pop_legacy_palette(kwds))
            self.assertEqual(kwds, {'other': 'stuff'})

    def test_color(self):
        kwds = {'color': COLORS.yellow, 'other': 'stuff'}
        pal = pop_legacy_palette(kwds)
        self.assertEqual(kwds, {'other': 'stuff'})
        self.assertEqual(pal, palette.Palette([COLORS.yellow]))

    def test_color(self):
        kwds = {'offColor': 'lime', 'other': 'stuff'}
        pal = pop_legacy_palette(kwds)
        self.assertEqual(kwds, {'other': 'stuff'})
        self.assertEqual(pal, palette.Palette([COLORS.red, COLORS.lime]))
