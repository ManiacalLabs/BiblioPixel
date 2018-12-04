"""
Fill in missing parts of a project and cleans up its sections
so they have exactly the right constructor.
"""

import copy
from . import aliases, construct, merge
from .. import layout
from .. util import deprecated, exception, log
from .. colors import make, palettes, tables
from .. animation.strip import Strip

DEFAULT_DRIVERS = [construct.to_type('simpixel')]


def fill(desc):
    desc = _fill_aliases(desc)
    desc = _fill_colors(desc)
    desc = _fill_palettes(desc)
    desc = _fill_animation(desc)
    desc = _fill_drivers(desc)
    desc = _fill_shape(desc)  # Must come after fill_drivers
    desc = _fill_numbers(desc)
    desc = _fill_controls(desc)

    return desc


def fill_layout(animation):
    # Try to fill in the layout if it's missing.
    # This is called from Project.__init__ - TODO: fix that.
    datatype = animation['datatype']

    args = getattr(datatype, 'LAYOUT_ARGS', Strip.LAYOUT_ARGS)
    layout_cl = getattr(datatype, 'LAYOUT_CLASS', Strip.LAYOUT_CLASS)

    args = {k: animation[k] for k in args if k in animation}
    return dict(args, datatype=layout_cl)


def _fill_aliases(desc):
    def unalias(k):
        if any(k.startswith(m) for m in aliases.ALIAS_MARKERS):
            return k[1:]
        return k

    al = desc.pop('aliases', {})
    aliases.PROJECT_ALIASES = {unalias(k): v for k, v in al.items()}
    return desc


def _fill_colors(desc):
    tables.set_user_colors(desc.pop('colors', {}))
    return desc


def _fill_palettes(desc):
    p = desc.pop('palettes', None)
    if p:
        default = p.pop('default', None)
        with exception.add('Error in "palettes" Section'):
            pp = {k: make.colors(v) for k, v in p.items()}
        palettes.PROJECT_PALETTES = pp
        if default:
            try:
                palettes.set_default(default)
            except:
                log.error('Unable to set default palette to be %s', default)
    return desc


def _fill_animation(desc):
    da = desc['animation'] or {'typename': 'animation'}
    da = construct.to_type_constructor(da, 'bibliopixel.animation')
    datatype = da.get('datatype')
    if not datatype:
        e = da.get('_exception')
        raise e or ValueError('Missing "datatype" in "animation" Section')

    da.setdefault('name', datatype.__name__)

    from .. animation import sequence
    if not issubclass(datatype, sequence.Sequence):
        # Magic here to allow this to work for non-sequences.
        length = da.pop('length', [])
        if length:
            desc.setdefault('run', {})['seconds'] = length[0]

    desc = merge.merge(getattr(datatype, 'PROJECT', {}), desc)

    da['run'] = dict(desc.pop('run', {}), **da.get('run', {}))
    desc['animation'] = da
    return desc


def _fill_drivers(desc):
    driver = construct.to_type(desc.pop('driver', {}))
    drivers = [construct.to_type(d) for d in desc['drivers']]
    if driver:
        drivers = [dict(driver, **d) for d in drivers or [{}]]

    desc['drivers'] = drivers or DEFAULT_DRIVERS
    return desc


def _fill_shape(desc):
    # TODO: this copy can't be deleted AND this can't be moved even one step
    # earlier without causing a test failure!
    desc = copy.deepcopy(desc)
    dimensions = desc.pop('dimensions', None)
    if dimensions:
        deprecated.deprecated('Project Section "dimensions"')

    shape = desc.pop('shape', None) or dimensions
    if not shape:
        return desc

    if len(desc['drivers']) != 1:
        raise ValueError('Cannot use dimensions with more than one driver')

    if isinstance(shape, int):
        shape = [shape]
    elif isinstance(shape, str):
        shape = shape.strip()
        if shape.startswith('(') and shape.endswith(')'):
            shape = shape[1:-1]
        try:
            shape = [int(s) for s in shape.split(',')]
        except:
            raise ValueError('Cannot parse shape %s' % shape)
    elif not isinstance(shape, (list, tuple)):
        raise ValueError('`shape` must be a number or a list, was "%s" (%s)' %
                         (shape, type(shape)))

    ldesc = construct.to_type_constructor(desc.get('layout') or {},
                                          python_path='bibliopixel.layout')
    driver = desc['drivers'][0]

    if len(shape) == 1:
        driver['num'] = shape[0]
        ldesc.setdefault('datatype', layout.strip.Strip)

    elif len(shape) == 2:
        driver['num'] = shape[0] * shape[1]
        ldesc.setdefault('datatype', layout.matrix.Matrix)
        ldesc.update(width=shape[0], height=shape[1])

    elif len(shape) == 3:
        driver['num'] = shape[0] * shape[1] * shape[2]
        ldesc.setdefault('datatype', layout.cube.Cube)
        ldesc.update(x=shape[0], y=shape[1], z=shape[2])

    else:
        raise ValueError('Dimension %s > 3' % len(shape))

    desc['layout'] = ldesc
    return desc


def _fill_numbers(desc):
    numbers = desc.pop('numbers', None) or 'python'
    if numbers != 'python':
        desc.setdefault('maker', {})['numpy_dtype'] = numbers

    return desc


def _fill_controls(desc):
    controls = desc.get('controls', None)
    if isinstance(controls, (str, dict)):
        desc['controls'] = [controls]
    return desc
