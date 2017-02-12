import unittest

import bibliopixel

from bibliopixel import (
    animation,
    colors,
    data_maker,
    font,
    gamepad,
    gamma,
    image,
    layout,
    led,
    log,
    matrix,
    return_codes,
    # serial_gamepad,
    timedata,
    util,
)

from bibliopixel.drivers import (
    APA102,
    LPD8806,
    # SimPixel,
    WS2801,
    driver_base,
    dummy_driver,
    hue,
    image_sequence,
    network,
    network_receiver,
    network_udp,
    serial_driver,
    spi_driver_base,
    # timedata_visualizer,
    visualizer,
    visualizerUI,
)


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        # We pass just by successfully importing everything above.
        pass
