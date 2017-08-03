import operator, os
from .. util import datafile

USER_ALIAS_FILE = os.path.expanduser('~/.bibliopixel_aliases')
USER_ALIASES = datafile.DataFile(USER_ALIAS_FILE)


BUILTIN_ALIASES = {
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


def get_alias(alias, external=False):
    value = not external and USER_ALIASES.get(alias)
    return value or BUILTIN_ALIASES.get(alias)


def print_alias(alias, value=None, print=print):
    value = value or get_alias(alias)
    if value:
        print('%s=%s' % (alias, value))
    else:
        print('# %s is not defined.' % alias)


def print_aliases(aliases, by_value=False, print=print):
    """
    Args:
        by_value: sort either by alias name, or by alias value
    """
    key_func = operator.itemgetter(int(by_value))
    for alias, value in sorted(aliases.items(), key=key_func):
        print_alias(alias, value, print)


set_alias = USER_ALIASES.set
delete_alias = USER_ALIASES.delete
