import operator, os, re
from .. util import log

ALIAS_MARKERS = '@$'
SEPARATORS = re.compile(r'([./#]|[^./#]+)')

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

    'bpa': 'BiblioPixelAnimations',
}


def get_alias(alias):
    return PROJECT_ALIASES.get(alias) or BUILTIN_ALIASES.get(alias)


def resolve(typename, aliases=None):
    aliases = aliases or {}

    def get(s):
        return aliases.get(s) or get_alias(s) or s

    def get_all(typename):
        for part in SEPARATORS.split(typename):
            is_alias = part and (part[0] in ALIAS_MARKERS)
            yield get(part[1:]) if is_alias else part

    return ''.join(get_all(get(typename)))
