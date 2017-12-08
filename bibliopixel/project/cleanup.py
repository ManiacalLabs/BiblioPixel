from . import construct, merge

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


def cleanup_animation(desc):
    if not desc.get('animation'):
        raise ValueError('Missing "animation" section')

    desc['animation'] = construct.to_type_constructor(
        desc['animation'], 'bibliopixel.animation', desc['aliases'])
    datatype = desc['animation'].get('datatype')
    if not datatype:
        raise ValueError('Missing "datatype" in "animation" section')
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

    desc['drivers'] = drivers or DEFAULT_DRIVERS[:]
    return desc
