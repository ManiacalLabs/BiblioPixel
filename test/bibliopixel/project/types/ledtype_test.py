from bibliopixel.drivers.ledtype import LEDTYPE
from . base import TypesBaseTest


class LEDTYPETypesTest(TypesBaseTest):
    def test_some(self):
        self.make('ledtype', 'LPD8806')
        self.make('ledtype', 'GENERIC')
        self.make('ledtype', LEDTYPE.NEOPIXEL)

        with self.assertRaises(ValueError):
            self.make('ledtype', 2)

        with self.assertRaises(KeyError):
            self.make('ledtype', 'NONE')
