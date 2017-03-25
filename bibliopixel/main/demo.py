import webbrowser

from bibliopixel.drivers.SimPixel import DriverSimPixel
from bibliopixel import LEDCircle, LEDMatrix, layout

HELP = """
Run a demo.  For the list of possible demos, type

  $ bibliopixel demo list

"""

SIMPIXEL_URL = 'http://beta.simpixel.io'
IMPORT_ERROR_TEXT = """
Please install the BiblioPixelAnimations library from here:

https://github.com/ManiacalLabs/BiblioPixelAnimations

"""


def bloom(args):
    driver = DriverSimPixel(args.width * args.height)
    led = LEDMatrix(driver, width=args.width, height=args.height)

    from BiblioPixelAnimations.matrix.bloom import Bloom
    return Bloom(led)


def circle(args):
    pixels_per = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
    rings, steps = layout.gen_circle(pixels_per=pixels_per)
    points = layout.layout_from_rings(rings, origin=(200, 200, 0), z_diff=8)
    driver = DriverSimPixel(sum(pixels_per), layout=points)
    led = LEDCircle(driver, rings=rings, maxAngleDiff=0)

    from BiblioPixelAnimations.circle.bloom import Bloom
    return Bloom(led)


def list_demos(args):
    print('Demos are', *sorted(DEMO_TABLE.keys()))


DEMO_TABLE = {
    'bloom': bloom,
    'circle': circle,
    'list': list_demos,
}


def run(args, settings):
    try:
        demo = DEMO_TABLE[args.name]
    except KeyError:
        raise KeyError('Unknown command %s' % args.name)
    try:
        anim = demo(args)
    except ImportError as e:
        if 'BiblioPixelAnimations' in e.msg:
            e.msg += IMPORT_ERROR_TEXT
        raise

    if not args.no_simpixel:
        webbrowser.open(SIMPIXEL_URL, new=0, autoraise=True)

    anim.run()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', nargs='?', default='bloom')
    parser.add_argument('-width', default=32, type=int)
    parser.add_argument('-height', default=32, type=int)
    parser.add_argument('-no_simpixel', action='store_true')
