import unittest
import bibliopixel
from bibliopixel.layout import geometry
from bibliopixel.project import data_maker
from bibliopixel.main import demo, main, run, set, show
from bibliopixel.remote import server

from bibliopixel import (
    animation,
    colors,
    font,
    gamma,
    image,
    layout,
    log,
    matrix,
    util,
)

from bibliopixel.controllers import (
    gamepad,
    # serial_gamepad,
)

from bibliopixel.drivers import (
    SPI,
    # SimPixel,
    driver_base,
    dummy_driver,
    hue,
    network,
    network_receiver,
    network_udp,
    return_codes,
    serial,
)


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        # We pass just by successfully importing everything above.
        pass
