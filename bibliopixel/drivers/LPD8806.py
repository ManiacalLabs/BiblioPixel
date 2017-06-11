from .. import gamma
from . channel_order import ChannelOrder
from . spi_driver_base import DriverSPIBase


class LPD8806(DriverSPIBase):
    """Main driver for LPD8806 based LED strips on devices like the Raspberry Pi
       and BeagleBone."""

    def __init__(self, num,
                 c_order=ChannelOrder.RGB,
                 spi_speed=2, gamma=gamma.LPD8806, **kwargs):
        super().__init__(num, c_order=c_order, spi_speed=spi_speed, gamma=gamma, **kwargs)

        # LPD8806 requires latch bytes at the end
        self._latchBytes = (self.numLEDs + 31) // 32
        for i in range(0, self._latchBytes):
            self._buf.append(0)

    # LPD8806 requires gamma correction and only supports 7-bits per channel
    # running each value through gamma will fix all of this.


# This is DEPRECATED.
DriverLPD8806 = LPD8806

MANIFEST = [
    {
        "id": "LPD8806",
        "class": LPD8806,
        "type": "driver",
        "display": "LPD8806 (SPI Native)",
        "desc": "Interface with LPD8806 strips over a native SPI port (Pi, BeagleBone, etc.)",
        "params": [{
            "id": "num",
            "label": "# Pixels",
            "type": "int",
            "default": 1,
            "min": 1,
            "help": "Total pixels in display."
        }, {
            "id": "c_order",
            "label": "Channel Order",
            "type": "combo",
            "options": {
                0: "RGB",
                1: "RBG",
                2: "GRB",
                3: "GBR",
                4: "BRG",
                5: "BGR"
            },
            "options_map": [
                [0, 1, 2],
                [0, 2, 1],
                [1, 0, 2],
                [1, 2, 0],
                [2, 0, 1],
                [2, 1, 0]
            ],
            "default": 0
        }, {
            "id": "dev",
            "label": "SPI Device Path",
            "type": "str",
            "default": "/dev/spidev0.0",
        }, {
            "id": "SPISpeed",
            "label": "SPI Speed (MHz)",
            "type": "int",
            "default": 2,
            "min": 1,
            "max": 24,
            "group": "Advanced"
        }]
    }
]
