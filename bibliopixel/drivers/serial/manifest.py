from ... import gamma
from . driver import DriverSerial, DriverTeensySmartMatrix

MANIFEST = [
    {
        "id": "serial",
        "class": DriverSerial,
        "type": "driver",
        "display": "Serial (AllPixel)",
        "desc": "Interface with USB Serial devices that support the AllPixel protocol.",
        "params": [{
                "id": "type",
                "label": "LED Type",
                "type": "combo",
                "options": {
                    0: "GENERIC",
                    1: "LPD8806",
                    2: "WS2801",
                    3: "WS281x/NEOPIXEL",
                    4: "WS2811_400",
                    5: "TM1804",
                    6: "TM1803",
                    7: "UCS1903",
                    8: "SM16716",
                    9: "APA102",
                    10: "LPD1886",
                    11: "P98131"
                },
            "default": 0
        }, {
            "id": "num",
            "label": "# Pixels",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Total pixels in display."
        }, {
            "id": "dev",
            "label": "Device Path",
            "type": "str",
            "default": "",
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
            "id": "SPISpeed",
            "label": "SPI Speed (MHz)",
            "type": "int",
            "default": 2,
            "min": 1,
            "max": 24,
            "group": "Advanced"
        }, {
            "id": "gamma",
            "label": "Gamma",
            "type": "combo",
            "default": None,
            "options": {
                    0: "LPD8806",
                    1: "APA102",
                    2: "WS2801",
                    3: "SM16716",
                    5: "WS281x"
            },
            "options_map": [
                gamma.LPD8806,
                gamma.APA102,
                gamma.WS2801,
                gamma.SM16716,
                gamma.WS2812B
            ]
        }, {
            "id": "restart_timeout",
            "label": "Restart Timeout",
            "type": "int",
            "default": 3,
            "min": 1,
            "group": "Advanced"
        }, {
            "id": "deviceID",
            "label": "Device ID",
            "type": "int",
            "default": None,
            "min": 0,
            "max": 255,
            "msg": "AllPixel ID",
            "group": "Advanced"
        }, {
            "id": "hardwareID",
            "label": "Hardware ID",
            "type": "str",
            "default": "1D50:60AB",
            "group": "Advanced"
        }, ]
    },
    {
        "id": "teensysmartmatrix",
        "class": DriverTeensySmartMatrix,
        "type": "driver",
        "display": "Teensy SmartMatrix",
        "desc": "Interface with Teensy SmartMatrix Controller.",
        "params": [{
            "id": "width",
            "label": "Width",
            "type": "int",
            "default": 32,
            "min": 16,
            "help": "Width of display. Firmware hardcoded."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 32,
            "min": 16,
            "help": "Width of display. Firmware hardcoded."
        }, {
            "id": "dev",
            "label": "Device Path",
            "type": "str",
            "default": "",
        }, {
            "id": "deviceID",
            "label": "Device ID",
            "type": "int",
            "default": None,
            "min": 0,
            "max": 255,
            "msg": "Teensy ID",
            "group": "Advanced"
        }, {
            "id": "hardwareID",
            "label": "Hardware ID",
            "type": "str",
            "default": "16C0:0483",
            "group": "Advanced"
        }, ]
    }
]
