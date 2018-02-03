import operator, os
from .. util import log

PROJECT_ALIASES = {}

BUILTIN_ALIASES = {
    # drivers
    'apa102': 'bibliopixel.drivers.SPI.APA102.APA102',
    'sk9822': 'bibliopixel.drivers.SPI.APA102.APA102',
    'dummy': 'bibliopixel.drivers.dummy_driver.Dummy',
    'hue': 'bibliopixel.drivers.hue.Hue',
    'lpd8806': 'bibliopixel.drivers.SPI.LPD8806.LPD8806',
    'mirror': 'bibliopixel.drivers.mirror.MirrorDriver',
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
    'split': 'bibliopixel.animation.split.Split',
    'receiver': 'bibliopixel.animation.receiver.BaseReceiver',
    'reprocess': 'bibliopixel.animation.reprocess.reprocess.Reprocess',
    'remote': 'bibliopixel.animation.remote.control.RemoteControl',
    'sequence': 'bibliopixel.animation.Sequence',
    'strip_test': 'bibliopixel.animation.tests.StripChannelTest',
}


def get_alias(alias):
    return PROJECT_ALIASES.get(alias) or BUILTIN_ALIASES.get(alias)
