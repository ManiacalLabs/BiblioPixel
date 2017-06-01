import random, webbrowser

from bibliopixel.drivers.SimPixel import SimPixel
from bibliopixel import Circle, Matrix, layout
from bibliopixel.animation import Sequence
from bibliopixel.project import project

HELP = """
Run a demo.  For the list of possible demos, type

  $ bibliopixel demo list

"""

DEFAULT_SIMPIXEL_URL = 'http://simpixel.io'

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
                'animation':
                'BiblioPixelAnimations.matrix.MatrixRain.MatrixRainBow',
                'run': {
                    'amt': 1,
                    'fps': 20,
                    'seconds': 8,
                },
            },
            {
                'animation': {
                    'typename': 'BiblioPixelAnimations.matrix.Text.ScrollText',
                    'xPos': 16,
                    'font_scale': 2,
                    'text': 'BiblioPixel Demo'
                },
                'run': {
                    'amt': 1,
                    'fps': 30,
                    'seconds': 8,
                    'until_complete': True,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.matrix.bloom.Bloom',
                'run': {
                    'amt': 3,
                    'fps': 60,
                    'seconds': 8,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.matrix.circlepop.CirclePop',
                'run': {
                    'amt': 1,
                    'fps': 30,
                    'seconds': 8,
                },
            },
        ],
    },
}

CUBE_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'led': {
        'typename': 'cube',
        'x': 0,
        'y': 0,
        'z': 0
    },

    'animation': {
        'typename': 'sequence',
        'animations': [
            {
                'animation': 'BiblioPixelAnimations.cube.Rain.RainBow',
                'run': {
                    'amt': 1,
                    'fps': 10,
                    'seconds': 8
                },
            },
            {
                'animation': 'BiblioPixelAnimations.cube.bloom.CubeBloom',
                'run': {
                    'amt': 6,
                    'fps': 20,
                    'seconds': 8,
                },
            }
        ],
    },
}


def matrix(args):
    driver = SimPixel(args.width * args.height)
    led = Matrix(driver, width=args.width, height=args.height)

    anim = Sequence(led)

    from BiblioPixelAnimations.matrix.MatrixRain import MatrixRainBow
    anim.add_animation(MatrixRainBow(led), amt=1, fps=20, seconds=8)

    from BiblioPixelAnimations.matrix.Text import ScrollText
    anim.add_animation(
        ScrollText(led, 'BiblioPixel Demo', xPos=args.width, font_scale=2),
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
    driver = SimPixel(sum(pixels_per), layout=points)
    led = Circle(driver, rings=rings, maxAngleDiff=0)

    from BiblioPixelAnimations.circle.bloom import CircleBloom
    return CircleBloom(led)


def make_runnable(demo, args):
    if callable(demo):
        return demo(args).run

    if 'driver' in demo:
        if not demo['driver'].get('num'):
            if 'led' in demo and demo['led']['typename'] == 'cube':
                demo['driver']['num'] = args.width * args.height * args.depth
            else:
                demo['driver']['num'] = args.width * args.height

    if 'led' in demo:
        led = demo['led']
        if 'width' in led:
            led['width'] = led['width'] or args.width
        if 'x' in led:
            led['x'] = led['x'] or args.width
        if 'height' in led:
            led['height'] = led['height'] or args.height
        if 'y' in led:
            led['y'] = led['y'] or args.height
        if 'z' in led:
            led['z'] = led['z'] or args.depth

    return project.project_to_runnable(demo)


DEMO_TABLE = {
    'bloom': BLOOM,
    'circle': circle,
    'matrix': matrix,
    'cube': CUBE_PROJECT,
    'matrix_project': MATRIX_PROJECT,
}

DEMO_OPTS = sorted(DEMO_TABLE.keys())


def usage():
    print('Available demos are: {}'.format(', '.join(DEMO_OPTS)))


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

    runnable = make_runnable(demo, args)
    if not args.simpixel.startswith('no'):
        webbrowser.open(args.simpixel, new=0, autoraise=True)

    runnable()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run demo in SimPixel'
    parser.add_argument('name', nargs='?', default='',
                        help='Name of demo to run. Options are: {}'.format(', '.join(DEMO_OPTS)))
    parser.add_argument('--width', default=16, type=int,
                        help='X dimension of display')
    parser.add_argument('--height', default=16, type=int,
                        help='Y dimension of display')
    parser.add_argument('--depth', default=16, type=int,
                        help='Z dimension of dipslay. Only used for Cube demos.')
    parser.add_argument('--simpixel', default=DEFAULT_SIMPIXEL_URL,
                        help='URL of SimPixel to use if not http://SimPixel.io')
