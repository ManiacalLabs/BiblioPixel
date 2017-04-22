import copy
from .importer import import_symbol

ALIASES = {
    'driver': {
        'apa102': 'bibliopixel.drivers.APA102.DriverAPA102',
        'dummy': 'bibliopixel.drivers.dummy_driver.DriverDummy',
        'hue': 'bibliopixel.drivers.hue.DriverHue',
        'image': 'bibliopixel.drivers.image_sequence.DriverImageSequence',
        'lpd8806': 'bibliopixel.drivers.LPD8806.DriverLPD8806',
        'network': 'bibliopixel.drivers.network.DriverNetwork',
        'network_udp': 'bibliopixel.drivers.network.DriverNetworkUDP',
        'simpixel': 'bibliopixel.drivers.SimPixel.DriverSimPixel',
        'ws2801': 'bibliopixel.drivers.WS2801.DriverWS2801',
    },

    'led': {
        'circle': 'bibliopixel.led.circle.LEDCircle',
        'cube': 'bibliopixel.led.cube.LEDCube',
        'matrix': 'bibliopixel.led.matrix.LEDMatrix',
        'pov': 'bibliopixel.led.pov.LEDPOV',
        'strip': 'bibliopixel.led.strip.LEDStrip',
    },

    'animation': {
        'off': 'bibliopixel.animation.off.OffAnim',
        'matrix_calibration':
        'bibliopixel.animation.tests.MatrixCalibrationTest',
        'matrix_test': 'bibliopixel.animation.tests.MatrixChannelTest',
        'receiver': 'bibliopixel.animation.receiver.BaseReceiver',
        'sequence': 'bibliopixel.animation.Sequence',
        'strip_test': 'bibliopixel.animation.tests.StripChannelTest',
    },
}


def resolve_aliases(project):
    def replace(item, key, aliases):
        if isinstance(item[key], str):
            item[key] = {'typename': item[key]}
        if 'typename' not in item[key]:
            return
        typename = item[key].get('typename')
        typename = aliases.get(typename, typename)
        item[key]['typename'] = typename
        typeclass = import_symbol(typename)
        if getattr(typeclass, 'IS_SEQUENCE', False):
            animations = item[key].get('animations', [])
            for i in range(len(animations)):
                replace(animations, i, aliases)

    result = copy.deepcopy(project)
    for key, aliases in ALIASES.items():
        (key in result) and replace(result, key, aliases)

    return result
