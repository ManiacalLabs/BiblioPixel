import webbrowser

from bibliopixel.drivers.SimPixel import DriverSimPixel
from bibliopixel import LEDMatrix

SIMPIXEL_URL = 'http://beta.simpixel.io'
IMPORT_ERROR_TEXT = """
Please install the BiblioPixelAnimations library from here:

https://github.com/ManiacalLabs/BiblioPixelAnimations

"""


def run(args):
    try:
        from BiblioPixelAnimations.matrix.bloom import Bloom
    except ImportError:
        raise ValueError(IMPORT_ERROR_TEXT)

    driver = DriverSimPixel(args.x * args.y)
    led = LEDMatrix(driver, width=args.x, height=args.y)
    anim = Bloom(led)

    webbrowser.open(SIMPIXEL_URL, new=0, autoraise=True)
    anim.run()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('-name', default='bloom')
    parser.add_argument('-x', default=32, type=int)
    parser.add_argument('-y', default=32, type=int)
