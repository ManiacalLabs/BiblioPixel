from . circle import LEDCircle
from . matrix import MatrixRotation, mapGen, MultiMapBuilder, LEDMatrix
from . pov import LEDPOV
from . strip import LEDStrip


MANIFEST = [
    {
        "id": "strip",
        "class": LEDStrip,
        "type": "controller",
        "control_type": "strip",
        "display": "LEDStrip",
        "params": [{
                "id": "threadedUpdate",
                "label": "Threaded Update",
                "type": "bool",
                "default": False,
                "help": "Enable to run display updates on a separate thread, which can improve speed."
        }, {
            "id": "masterBrightness",
            "label": "Master Brightness",
            "type": "int",
            "min": 1,
            "max": 255,
            "default": 255,
            "help": "Master brightness for display, 0-255"
        }, {
            "id": "pixelWidth",
            "label": "Pixel Width",
            "group": "Advanced",
            "type": "int",
            "min": 1,
            "default": 1,
            "help": "Pixel scaling amount. Setting to >1 will make each logical pixel N LEDs in width."
        }, ]
    },
    {
        "id": "matrix",
        "class": LEDMatrix,
        "type": "controller",
        "control_type": "matrix",
        "display": "LEDMatrix",
        "params": [{
                "id": "width",
                "label": "Width",
                "type": "int",
                "default": 0,
                "min": 0,
                "help": "Width of display. Leave this and Height as 0 to get from driver."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Height of display. Leave this and Width as 0 to get from driver."
        }, {
            "id": "rotation",
            "label": "Rotation",
            "type": "combo",
            "options": {
                    0: "0&deg;",
                    3: "90&deg;",
                    2: "180&deg;",
                    1: "270&deg;",
            },
            "default": 0,
            "help": "Amount to rotate matrix by."
        }, {
            "id": "vert_flip",
            "label": "Vertical Flip",
            "type": "bool",
            "default": False,
            "help": "Flip the display over the x-axis.",
        }, {
            "id": "serpentine",
            "label": "Serpentine",
            "type": "bool",
            "default": True,
            "help": "Use a serpentine layout for the pixel map when auto-generated.",
        }, {
            "id": "threadedUpdate",
            "label": "Threaded Update",
            "type": "bool",
            "default": False,
            "help": "Enable to run display updates on a separate thread, which can improve speed."
        }, {
            "id": "masterBrightness",
            "label": "Master Brightness",
            "type": "int",
            "min": 1,
            "max": 255,
            "default": 255,
            "help": "Master brightness for display, 0-255"
        }, {
            "id": "pixelSize",
            "label": "Pixel Size",
            "group": "Advanced",
            "type": "multi",
            "controls": [
                    {
                        "label": "Width",
                        "type": "int",
                        "min": 1,
                        "default": 1,
                        "help": "Logical Pixel Width"
                    }, {
                        "label": "Height",
                        "type": "int",
                        "min": 1,
                        "default": 1,
                        "help": "Logical Pixel Height"
                    },
            ],
            "default": [1, 1],
            "help":"Pixel scaling amount. Each logical pixel will be Width*Height LEDs in size."
        }, ]
    }
]
