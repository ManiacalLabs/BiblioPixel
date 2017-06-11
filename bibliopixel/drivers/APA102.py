from . channel_order import ChannelOrder
from . spi_driver_base import DriverSPIBase


class APA102(DriverSPIBase):
    """Main driver for APA102 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.RGB, **kwargs):
        super().__init__(num, c_order=c_order, **kwargs)

        # APA102 requires latch bytes at the end
        self._latchBytes = (int(num / 64.0) + 1)

    def _render(self):
        super()._render()
        newBuf = [0xFF] * (self.bufByteCount() + self.numLEDs)
        newBuf[1::4] = self._buf[0::3]
        newBuf[2::4] = self._buf[1::3]
        newBuf[3::4] = self._buf[2::3]
        self._buf[:] = [0, 0, 0, 0] + newBuf
        self._buf.extend([0xFF, 0, 0, 0] * self._latchBytes)


# This is DEPRECATED.
DriverAPA102 = APA102

MANIFEST = [
    {
        "id": "APA102",
        "class": APA102,
        "type": "driver",
        "display": "APA102 (SPI Native)",
        "desc": "Interface with APA102 strips over a native SPI port (Pi, BeagleBone, etc.)",
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
        }, {
            "id": "use_py_spi",
            "label": "Use PySPI",
            "type": "bool",
            "default": True,
            "group": "Advanced"
        }]
    }
]
