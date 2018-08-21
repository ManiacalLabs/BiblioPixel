"""
Fill in missing parts of a project and cleans up its sections
so they have exactly the right constructor.
"""

import copy
from . import aliases, alias_lists, construct, merge
from .. import layout, util
from .. animation.strip import BaseStripAnim

DEFAULT_DRIVERS = [construct.to_type('simpixel')]


def fill(desc):
    desc = _fill_aliases(desc)
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

    args = getattr(datatype, 'LAYOUT_ARGS', BaseStripAnim.LAYOUT_ARGS)
    layout_cl = getattr(datatype, 'LAYOUT_CLASS', BaseStripAnim.LAYOUT_CLASS)

    args = {k: animation[k] for k in args if k in animation}
    return dict(args, datatype=layout_cl)


def _fill_aliases(desc):
    def unalias(k):
        if any(k.startswith(m) for m in aliases.ALIAS_MARKERS):
            return k[1:]
        return k

    al = desc.pop('aliases', {})
    alias_lists.PROJECT_ALIASES = {unalias(k): v for k, v in al.items()}
    return desc


def _fill_animation(desc):
    if not desc['animation']:
        raise ValueError('Missing "animation" section')

    desc['animation'] = construct.to_type_constructor(
        desc['animation'], 'bibliopixel.animation')
    datatype = desc['animation'].get('datatype')
    if not datatype:
        e = desc['animation'].get('_exception')
        raise e or ValueError('Missing "datatype" in "animation" section')

    desc['animation'].setdefault('name', datatype.__name__)

    from .. animation import sequence
    if not issubclass(datatype, sequence.Sequence):
        # Magic here to allow this to work for non-sequences.
        length = desc['animation'].pop('length', [])
        if length:
            desc['run']['seconds'] = length[0]

    desc = merge.merge(getattr(datatype, 'PROJECT', {}), desc)

    run = desc.pop('run')
    anim_run = desc['animation'].setdefault('run', {})
    if run:
        desc['animation']['run'] = dict(run, **anim_run)
    return desc


def _fill_drivers(desc):
    driver = construct.to_type(desc.pop('driver', {}))
    drivers = [construct.to_type(d) for d in desc['drivers']]
    if driver:
        if drivers:
            drivers = [dict(driver, **d) for d in drivers]
        else:
            drivers = [driver]

    desc['drivers'] = drivers or DEFAULT_DRIVERS
    return desc


def _fill_shape(desc):
    desc = copy.deepcopy(desc)
    dimensions = desc.pop('dimensions', None)
    if dimensions:
        util.deprecated.deprecated('Project section "dimensions"')

    shape = desc.pop('shape', None) or dimensions
    if not shape:
        return desc

    if len(desc['drivers']) != 1:
        raise ValueError('Cannot use dimensions with more than one driver')

    if isinstance(shape, int):
        shape = [shape]
    elif not isinstance(shape, list):
        raise ValueError('`shape` must be a number or a list, was "%s"' % shape)

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
    numbers = desc.pop('numbers', 'python')
    if numbers != 'python':
        desc.setdefault('maker', {})['numpy_dtype'] = numbers

    return desc


def _fill_controls(desc):
    controls = desc.get('controls', None)
    if isinstance(controls, (str, dict)):
        desc['controls'] = [controls]
    return desc
