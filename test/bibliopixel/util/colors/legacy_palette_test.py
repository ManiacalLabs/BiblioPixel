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
        kwds = {'palette': pal, 'other': 'stuff'}
        self.assertIs(pal, pop_legacy_palette(kwds))
        self.assertEqual(kwds, {'other': 'stuff'})

    def test_color(self):
        kwds = {'color': COLORS.yellow, 'other': 'stuff'}
        pal = pop_legacy_palette(kwds, ('color', COLORS.green))
        self.assertEqual(kwds, {'other': 'stuff'})
        self.assertEqual(pal, palette.Palette([COLORS.yellow]))

        pal = pop_legacy_palette(kwds, ('color', COLORS.green))
        self.assertEqual(pal, palette.Palette([COLORS.green]))

    def test_colors(self):
        colors = [COLORS.red, COLORS.lime, COLORS.orange]
        kwds = {'colors': colors, 'other': 'stuff'}
        pal = pop_legacy_palette(kwds, ('colors', [COLORS.black]))
        self.assertEqual(kwds, {'other': 'stuff'})
        self.assertEqual(pal, palette.Palette(colors))

        pal = pop_legacy_palette(kwds, ('palette', [COLORS.black]))
        self.assertEqual(pal, palette.Palette([COLORS.black]))

    def test_errors(self):
        kwds = {'colors': 12, 'palette': 'stuff', 'color': 'stuff'}
        with self.assertRaises(ValueError):
            pop_legacy_palette(kwds, ('colors', [COLORS.black]))
        with self.assertRaises(ValueError):
            pop_legacy_palette(kwds, ('color', COLORS.black))
