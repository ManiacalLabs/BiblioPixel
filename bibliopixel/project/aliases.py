import copy
from .importer import import_symbol

ALIASES = {
    # drivers
    'apa102': 'bibliopixel.drivers.API.APA102.APA102',
    'sk9822': 'bibliopixel.drivers.API.APA102.APA102',
    'dummy': 'bibliopixel.drivers.dummy_driver.Dummy',
    'hue': 'bibliopixel.drivers.hue.Hue',
    'image': 'bibliopixel.drivers.image_sequence.ImageSequence',
    'lpd8806': 'bibliopixel.drivers.API.LPD8806.LPD8806',
    'network': 'bibliopixel.drivers.network.Network',
    'network_udp': 'bibliopixel.drivers.network.NetworkUDP',
    'serial': 'bibliopixel.drivers.serial.Serial',
    'simpixel': 'bibliopixel.drivers.SimPixel.SimPixel',
    'ws281x': 'bibliopixel.drivers.API.WS281X.WS281X',
    'ws2801': 'bibliopixel.drivers.API.WS2801.WS2801',
    'spi': 'bibliopixel.drivers.SPI.SPI',
    'pi_ws281x': 'bibliopixel.drivers.PiWS281X.PiWS281X',

    # layouts
    'circle': 'bibliopixel.layout.circle.Circle',
    'cube': 'bibliopixel.layout.cube.Cube',
    'matrix': 'bibliopixel.layout.matrix.Matrix',
    'pov': 'bibliopixel.layout.pov.POV',
    'strip': 'bibliopixel.layout.strip.Strip',

    # animations
    'off': 'bibliopixel.animation.off.OffAnim',
    'remote': 'bibliopixel.remote.control.RemoteControl',
    'matrix_calibration':
    'bibliopixel.animation.tests.MatrixCalibrationTest',
    'matrix_test': 'bibliopixel.animation.tests.MatrixChannelTest',
    'receiver': 'bibliopixel.animation.receiver.BaseReceiver',
    'sequence': 'bibliopixel.animation.Sequence',
    'strip_test': 'bibliopixel.animation.tests.StripChannelTest',
}


def resolve(*dicts):
    """Resolve aliases and merge.  Evaluation proceeds from left to right."""
    def resolver(value):
        if isinstance(value, str):
            value = {'typename': value}
        else:
            value = copy.deepcopy(value)

        typename = value.get('typename')
        if typename:
            value['typename'] = ALIASES.get(typename.lower(), typename)

        return value

    result = {}

    for d in dicts:
        for key, value in d.items():
            if key == 'drivers':
                result['drivers'] = [resolver(d) for d in value]
            else:
                result.setdefault(key, {}).update(**resolver(value))

    return result
