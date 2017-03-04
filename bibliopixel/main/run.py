from bibliopixel.util import project

HELP = """
Run a project description file.
"""

DEFAULT_PROJECT = """
{
    "driver": {
        "typename": "bibliopixel.drivers.SimPixel.DriverSimPixel",
        "num": 1024
    },

    "led": {
        "typename": "bibliopixel.led.matrix.LEDMatrix",
        "width": 32,
        "height": 32
    },

    "animation": {
        "typename": "BiblioPixelAnimations.matrix.bloom.Bloom"
    }
}

"""


def run(args):
    data = open(args.name).read() if args.name else DEFAULT_PROJECT
    project.run(data)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', nargs='?')
