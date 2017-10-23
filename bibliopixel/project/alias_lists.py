import operator, os
from .. util import datafile, log

USER_ALIAS_FILE = os.path.expanduser('~/.bibliopixel_aliases')
USER_ALIASES = datafile.DataFile(USER_ALIAS_FILE)


BUILTIN_ALIASES = {
    # drivers
    'apa102': 'bibliopixel.drivers.SPI.APA102.APA102',
    'sk9822': 'bibliopixel.drivers.SPI.APA102.APA102',
    'dummy': 'bibliopixel.drivers.dummy_driver.Dummy',
    'hue': 'bibliopixel.drivers.hue.Hue',
    'lpd8806': 'bibliopixel.drivers.SPI.LPD8806.LPD8806',
    'network': 'bibliopixel.drivers.network.Network',
    'network_udp': 'bibliopixel.drivers.network_udp.NetworkUDP',
    'serial': 'bibliopixel.drivers.serial.Serial',
    'simpixel': 'bibliopixel.drivers.SimPixel.SimPixel',
    'ws281x': 'bibliopixel.drivers.SPI.WS281X.WS281X',
    'ws2801': 'bibliopixel.drivers.SPI.WS2801.WS2801',
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
    'feedback': 'bibliopixel.animation.feedback.Feedback',
    'matrix_calibration': 'bibliopixel.animation.tests.MatrixCalibrationTest',
    'matrix_test': 'bibliopixel.animation.tests.MatrixChannelTest',
    'mixer': 'bibliopixel.animation.mixer.Mixer',
    'receiver': 'bibliopixel.animation.receiver.BaseReceiver',
    'reprocess': 'bibliopixel.animation.reprocess.reprocess.Reprocess',
    'remote': 'bibliopixel.remote.control.RemoteControl',
    'sequence': 'bibliopixel.animation.Sequence',
    'strip_test': 'bibliopixel.animation.tests.StripChannelTest',
}


def get_alias(alias, isolate=False):
    return not isolate and USER_ALIASES.get(alias) or BUILTIN_ALIASES.get(alias)


def print_alias(alias, value, printer=log.printer):
    if value:
        printer('%s = %s' % (alias, value))
    else:
        printer('# %s is not defined.' % alias)


def print_aliases(builtin, by_value=False, printer=log.printer):
    """
    Args:
        by_value: sort either by alias name, or by alias value
    """

    aliases = BUILTIN_ALIASES if builtin else USER_ALIASES.data
    if not aliases:
        printer('(no aliases)')
        return

    key_func = operator.itemgetter(int(by_value))
    for alias, value in sorted(aliases.items(), key=key_func):
        print_alias(alias, value, print)


set_alias = USER_ALIASES.set
delete_alias = USER_ALIASES.delete
delete_all_alias = USER_ALIASES.delete_all
