import copy
from . import alias_lists, construct, merge
from .. import layout, util

DEFAULT_DRIVERS = [construct.to_type('simpixel')]


def cleanup_layout(animation):
    # Try to fill in the layout if it's missing.
    datatype = animation['datatype']

    try:
        args = datatype.LAYOUT_ARGS
        layout_cl = datatype.LAYOUT_CLASS
    except:
        raise ValueError('Missing "layout" section')

    args = {k: animation[k] for k in args if k in animation}
    return dict(args, datatype=layout_cl)


def cleanup_aliases(desc):
    alias_lists.PROJECT_ALIASES = desc.pop('aliases', {})
    return desc


def cleanup_numbers(desc):
    numbers = desc.pop('numbers', 'python')
    if numbers != 'python':
        desc.setdefault('maker', {})['numpy_dtype'] = numbers

    return desc


def cleanup_animation(desc):
    if not desc['animation']:
        raise ValueError('Missing "animation" section')

    desc['animation'] = construct.to_type_constructor(
        desc['animation'], 'bibliopixel.animation')
    datatype = desc['animation'].get('datatype')
    if not datatype:
        raise ValueError('Missing "datatype" in "animation" section')

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


def cleanup_drivers(desc):
    driver = construct.to_type(desc.pop('driver', {}))
    drivers = [construct.to_type(d) for d in desc['drivers']]
    if driver:
        if drivers:
            drivers = [dict(driver, **d) for d in drivers]
        else:
            drivers = [driver]

    desc['drivers'] = drivers or DEFAULT_DRIVERS
    return desc


def cleanup_shape(desc):
    desc = copy.deepcopy(desc)
    dimensions = desc.pop('dimensions', None)
    if dimensions:
        util.deprecated.deprecated('Project section "dimensions"')

    shape = desc.pop('shape', None) or dimensions
    if not shape:
        return desc

    if len(desc['drivers']) != 1:
        raise ValueError('Cannot use dimensions with more than one driver')

    try:
        d = [int(shape)]
    except:
        d = list(shape)

    ldesc = construct.to_type_constructor(desc.get('layout') or {},
                                          python_path='bibliopixel.layout')
    driver = desc['drivers'][0]

    if len(d) == 1:
        driver['num'] = d[0]
        ldesc.setdefault('datatype', layout.strip.Strip)

    elif len(d) == 2:
        driver['num'] = d[0] * d[1]
        ldesc.setdefault('datatype', layout.matrix.Matrix)
        ldesc.update(width=d[0], height=d[1])

    elif len(d) == 3:
        driver['num'] = d[0] * d[1] * d[2]
        ldesc.setdefault('datatype', layout.cube.Cube)
        ldesc.update(x=d[0], y=d[1], z=d[2])

    else:
        raise ValueError('Dimension %s > 3' % len(d))

    desc['layout'] = ldesc
    return desc


def cleanup(desc):
    desc = cleanup_aliases(desc)
    desc = cleanup_animation(desc)
    desc = cleanup_drivers(desc)
    desc = cleanup_shape(desc)  # Must come after cleanup_drivers
    desc = cleanup_numbers(desc)

    return desc
