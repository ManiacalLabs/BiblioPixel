import webbrowser

from bibliopixel.drivers.SimPixel import DriverSimPixel
from bibliopixel import LEDCircle, LEDMatrix, layout
from bibliopixel.animation import AnimationQueue

HELP = """
Run a demo.  For the list of possible demos, type

  $ bibliopixel demo list

"""

DEFAULT_SIMPIXEL_URL = 'http://simpixel.io'
IMPORT_ERROR_TEXT = """
Please install the BiblioPixelAnimations library from here:

https://github.com/ManiacalLabs/BiblioPixelAnimations

"""


def matrix(args):
    driver = DriverSimPixel(args.width * args.height)
    led = LEDMatrix(driver, width=args.width, height=args.height)

    anim = AnimationQueue(led, anims=None)

    from BiblioPixelAnimations.matrix.MatrixRain import MatrixRainBow
    anim.addAnim(MatrixRainBow(led), amt=1, fps=20, seconds=8)

    from BiblioPixelAnimations.matrix.Text import ScrollText
    anim.addAnim(ScrollText(led, 'BiblioPixel Demo', xPos=args.width, font_scale=4),
                 amt=1, fps=30, until_complete=True)

    from BiblioPixelAnimations.matrix.bloom import Bloom
    anim.addAnim(Bloom(led), amt=3, fps=60, seconds=8)

    from BiblioPixelAnimations.matrix.circlepop import CirclePop
    anim.addAnim(CirclePop(led), amt=1, fps=30, seconds=8)

    return anim


def circle(args):
    pixels_per = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
    rings, steps = layout.gen_circle(pixels_per=pixels_per)
    points = layout.layout_from_rings(rings, origin=(200, 200, 0), z_diff=8)
    driver = DriverSimPixel(sum(pixels_per), layout=points)
    led = LEDCircle(driver, rings=rings, maxAngleDiff=0)

    from BiblioPixelAnimations.circle.bloom import CircleBloom
    return CircleBloom(led)


DEMO_TABLE = {
    'matrix': matrix,
    'circle': circle,
}


def run(args, settings):
    try:
        if args.name == 'list':
            print('Available demos are:\n  ' + '\n  '.join(sorted(DEMO_TABLE.keys())))
            return
        else:
            demo = DEMO_TABLE[args.name]
    except KeyError:
        raise KeyError('Unknown demo %s' % args.name)
    try:
        anim = demo(args)
    except ImportError as e:
        if 'BiblioPixelAnimations' in e.msg:
            e.msg += IMPORT_ERROR_TEXT
        raise

    if not args.simpixel.startswith('no'):
        webbrowser.open(args.simpixel, new=0, autoraise=True)

    anim.run()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', nargs='?', default='matrix')
    parser.add_argument('--width', default=32, type=int)
    parser.add_argument('--height', default=32, type=int)
    parser.add_argument('--simpixel', default=DEFAULT_SIMPIXEL_URL)
