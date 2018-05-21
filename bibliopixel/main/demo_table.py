from bibliopixel.drivers.SimPixel import SimPixel
from bibliopixel import Circle, Matrix
from bibliopixel.layout import geometry
from bibliopixel.animation import Sequence
from BiblioPixelAnimations.circle.bloom import CircleBloom
from BiblioPixelAnimations.circle.swirl import Swirl
from BiblioPixelAnimations.circle.hyperspace import HyperspaceRainbow


BLOOM = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'layout': {
        'typename': 'matrix',
        'width': 0,
        'height': 0,
    },

    'animation': {
        'typename': 'BiblioPixelAnimations.matrix.bloom.Bloom'
    },

    'run': {
        'amt': 6,
        'fps': 30
    }
}


MATRIX_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'layout': {
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
                    'fps': 20,
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
                    'fps': 15,
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

    'layout': {
        'typename': 'cube',
        'x': 0,
        'y': 0,
        'z': 0
    },

    'animation': {
        'typename': 'sequence',
        'animations': [
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.cube.wave_spiral.WaveSpiral',
                    'dir': False,
                    'offset': 6
                },
                'run': {
                    'amt': 1,
                    'fps': 15,
                    'seconds': 8
                },
            },
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

_PIXELS_PER = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
_RINGS, _STEPS = geometry.make_circle_coord_map(pixels_per=_PIXELS_PER)
_POINTS = geometry.make_circle_coord_map_positions(
    _RINGS, origin=(200, 200, 0), z_diff=16)

CIRCLE_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': sum(_PIXELS_PER),
        'pixel_positions': _POINTS,
    },

    'layout': {
        'typename': 'circle',
        'rings': _RINGS,
        'maxAngleDiff': 0,
    },

    'animation': {
        'typename': 'sequence',
        'length': 8,
        'animations': [CircleBloom, Swirl, HyperspaceRainbow]
    }
}


def circle(args):
    pixels_per = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
    rings, steps = geometry.make_circle_coord_map(pixels_per=pixels_per)
    points = geometry.make_circle_coord_map_positions(
        rings, origin=(200, 200, 0), z_diff=16)
    driver = SimPixel(sum(pixels_per), pixel_positions=points)
    layout = Circle(driver, rings=rings, maxAngleDiff=0)
    anim = Sequence(layout)

    anim.add_animation(CircleBloom(layout), amt=3, fps=30, seconds=8)
    anim.add_animation(Swirl(layout, angle=4), amt=6, fps=15, seconds=8)
    anim.add_animation(HyperspaceRainbow(layout), fps=15, seconds=8)

    return anim


DEMO_TABLE = {
    'bloom': BLOOM,
    'circle': CIRCLE_PROJECT,
    'cube': CUBE_PROJECT,
    'matrix': MATRIX_PROJECT,
}
