import operator, os
from .. util import log

PROJECT_ALIASES = {}

BUILTIN_ALIASES = {
    'apa102': 'bibliopixel.drivers.SPI.APA102.APA102',
    'lpd8806': 'bibliopixel.drivers.SPI.LPD8806.LPD8806',
    'pi_ws281x': 'bibliopixel.drivers.PiWS281X.PiWS281X',
    'serial': 'bibliopixel.drivers.serial.Serial',
    'sk9822': 'bibliopixel.drivers.SPI.APA102.APA102',
    'spi': 'bibliopixel.drivers.SPI.SPI',
    'ws2801': 'bibliopixel.drivers.SPI.WS2801.WS2801',
    'ws281x': 'bibliopixel.drivers.SPI.WS281X.WS281X',

    'reprocess': 'bibliopixel.animation.reprocess.reprocess.Reprocess',
}


def get_alias(alias):
    return PROJECT_ALIASES.get(alias) or BUILTIN_ALIASES.get(alias)
