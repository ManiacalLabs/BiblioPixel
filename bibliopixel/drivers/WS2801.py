from . channel_order import ChannelOrder
from . spi_driver_base import DriverSPIBase
from .. import gamma


class WS2801(DriverSPIBase):
    """Main driver for WS2801 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.RGB,
                 spi_speed=1, gamma=gamma.WS2801, **kwargs):
        if spi_speed > 1 or spi_speed <= 0:
            raise ValueError(
                "WS2801 requires an SPI speed no greater than 1MHz or SPI speed was set <= 0")
        super().__init__(num, c_order=c_order, spi_speed=spi_speed,
                         gamma=gamma, **kwargs)


# This is DEPRECATED.
DriverWS2801 = WS2801

MANIFEST = [
    {
        "id": "WS2801",
        "class": WS2801,
        "type": "driver",
        "display": "WS2801 (SPI Native)",
        "desc": "Interface with WS2801 strips over a native SPI port (Pi, BeagleBone, etc.)",
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
        }]
    }
]
