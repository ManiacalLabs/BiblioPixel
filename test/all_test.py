import unittest
import bibliopixel
from bibliopixel.main import demo, main, run, set, show

from bibliopixel import (
    animation,
    colors,
    data_maker,
    font,
    gamepad,
    gamma,
    image,
    layout,
    log,
    matrix,
    return_codes,
    # serial_gamepad,
    util,
)

from bibliopixel.layout import geometry

from bibliopixel.drivers import (
    SPI,
    # SimPixel,
    driver_base,
    dummy_driver,
    hue,
    network,
    network_receiver,
    network_udp,
    serial,
    # timedata_visualizer,
)


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        # We pass just by successfully importing everything above.
        pass
