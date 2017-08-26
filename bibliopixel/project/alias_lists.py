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
    'network_udp': 'bibliopixel.drivers.network_udp.NetworkUDP',
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


def get_alias(alias, isolate=False):
    return (not isolate and USER_ALIASES.get(alias) or
            BUILTIN_ALIASES.get(alias))


def print_alias(alias, value, print=print):
    if value:
        print('%s = %s' % (alias, value))
    else:
        print('# %s is not defined.' % alias)


def print_aliases(builtin, by_value=False, print=print):
    """
    Args:
        by_value: sort either by alias name, or by alias value
    """

    aliases = BUILTIN_ALIASES if builtin else USER_ALIASES.data
    if not aliases:
        print('(no aliases)')
        return

    key_func = operator.itemgetter(int(by_value))
    for alias, value in sorted(aliases.items(), key=key_func):
        print_alias(alias, value, print)


set_alias = USER_ALIASES.set
delete_alias = USER_ALIASES.delete
delete_all_alias = USER_ALIASES.delete_all
