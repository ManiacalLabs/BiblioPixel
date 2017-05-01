import random, webbrowser

from bibliopixel.drivers.SimPixel import DriverSimPixel
from bibliopixel import LEDCircle, LEDMatrix, layout
from bibliopixel.animation import Sequence
from bibliopixel.project import project

HELP = """
Run a demo.  For the list of possible demos, type

  $ bibliopixel demo list

"""

DEFAULT_SIMPIXEL_URL = 'http://simpixel.io'
IMPORT_ERROR_TEXT = """
Please install the BiblioPixelAnimations library from here:

https://github.com/ManiacalLabs/BiblioPixelAnimations

"""

BLOOM = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'led': {
        'typename': 'matrix',
        'width': 0,
        'height': 0,
    },

    'animation': {
        'typename': 'BiblioPixelAnimations.matrix.bloom.Bloom'
    },
}


MATRIX_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'led': {
        'typename': 'matrix',
        'width': 0,
        'height': 0,
    },

    'animation': {
        'typename': 'sequence',
        'animations': [
            {
                'typename':
                'BiblioPixelAnimations.matrix.MatrixRain.MatrixRainBow',
                'run': {
                    'amt': 1,
                    'fps': 20,
                    'seconds': 8,
                },
            },
            {
                'typename': 'BiblioPixelAnimations.matrix.Text.ScrollText',
                'xPos': 32,
                'font_scale': 4,
                'text': 'BiblioPixel Demo',
                'run': {
                    'amt': 1,
                    'fps': 30,
                    'seconds': 8,
                    'until_complete': True,
                },
            },
            {
                'typename': 'BiblioPixelAnimations.matrix.bloom.Bloom',
                'run': {
                    'amt': 3,
                    'fps': 60,
                    'seconds': 8,
                },
            },
            {
                'typename': 'BiblioPixelAnimations.matrix.circlepop.CirclePop',
                'run': {
                    'amt': 1,
                    'fps': 30,
                    'seconds': 8,
                },
            },
        ],
    },
}


def make_runnable(demo, args):
    if callable(demo):
        return demo(args).run

    if 'driver' in demo:
        if not demo['driver'].get('num'):
            demo['driver']['num'] = args.width * args.height

    if 'led' in demo:
        led = demo['led']
        if 'width' in led:
            led['width'] = led['width'] or args.width
        if 'height' in led:
            led['height'] = led['height'] or args.height

    return project.make_runnable(**demo)


def matrix(args):
    driver = DriverSimPixel(args.width * args.height)
    led = LEDMatrix(driver, width=args.width, height=args.height)

    anim = Sequence(led)

    from BiblioPixelAnimations.matrix.MatrixRain import MatrixRainBow
    anim.add_animation(MatrixRainBow(led), amt=1, fps=20, seconds=8)

    from BiblioPixelAnimations.matrix.Text import ScrollText
    anim.add_animation(
        ScrollText(led, 'BiblioPixel Demo', xPos=args.width, font_scale=4),
        amt=1, fps=30, until_complete=True)

    from BiblioPixelAnimations.matrix.bloom import Bloom
    anim.add_animation(Bloom(led), amt=3, fps=60, seconds=8)

    from BiblioPixelAnimations.matrix.circlepop import CirclePop
    anim.add_animation(CirclePop(led), amt=1, fps=30, seconds=8)

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
    'bloom': BLOOM,
    'circle': circle,
    'matrix': matrix,
    'matrix_project': MATRIX_PROJECT,
}


def usage():
    print('Available demos are:', *sorted(DEMO_TABLE.keys()))


def run(args, settings):
    if args.name == 'list':
        usage()
        return

    if not args.name:
        usage()
        args.name = random.choice(list(DEMO_TABLE))
        print('Selected', args.name)

    try:
        demo = DEMO_TABLE[args.name]
    except KeyError:
        raise KeyError('Unknown demo %s' % args.name)

    try:
        runnable = make_runnable(demo, args)
    except ImportError as e:
        if 'BiblioPixelAnimations' in e.msg:
            e.msg += IMPORT_ERROR_TEXT
        raise

    if not args.simpixel.startswith('no'):
        webbrowser.open(args.simpixel, new=0, autoraise=True)

    runnable()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', nargs='?', default='')
    parser.add_argument('--width', default=32, type=int)
    parser.add_argument('--height', default=32, type=int)
    parser.add_argument('--simpixel', default=DEFAULT_SIMPIXEL_URL)
