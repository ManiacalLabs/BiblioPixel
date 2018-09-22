from . base import TypesBaseTest
from bibliopixel import gamma


class GammaTypesTest(TypesBaseTest):
    def test_some(self):
        self.make('gamma', 'LPD8806', gamma.LPD8806)
        self.make('gamma', 'DEFAULT', gamma.DEFAULT)

        gam = self.make('gamma', {'gamma': 2.5, 'offset': 0.5})
        self.assertEqual(gam['gamma'].table, gamma.APA102.table)

        gam = self.make('gamma', [2.5, 0.5, 128])
        self.assertEqual(gam['gamma'].table, gamma.LPD8806.table)

        with self.assertRaises(TypeError):
            self.make('gamma', [0, 1, 2, 3])

        with self.assertRaises(ValueError):
            self.make('gamma', None)
