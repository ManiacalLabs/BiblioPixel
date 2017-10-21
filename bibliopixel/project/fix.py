from . import construct

DEFAULT_DRIVERS = [construct.to_type('simpixel')]


def fix_drivers(project):
    # This must be called before recursing into the children.
    driver = construct.to_type(project.pop('driver', {}))
    drivers = [construct.to_type(d) for d in project.get('drivers', [])]
    if driver:
        if drivers:
            drivers = [dict(driver, **d) for d in drivers]
        else:
            drivers = [driver]

    project['drivers'] = drivers or DEFAULT_DRIVERS


def fix_layout_and_animation(project):
    # This must be called after recursing into children.
    anim = project.get('run_animation', {}).get('animation')
    if not anim:
        raise ValueError('Missing "animation" section')

    anim_datatype = anim.get('datatype')
    if not anim_datatype:
        raise ValueError('Missing "datatype" in "animation" section')

    layout = project.get('layout')
    if layout:
        if not layout.get('datatype'):
            raise ValueError('Missing "datatype" in "layout" section')
        return

    # Try to fill in the layout if it's missing.
    try:
        args, layout_cl = anim_datatype.LAYOUT_ARGS, anim_datatype.LAYOUT_CLASS
    except:
        raise ValueError('Missing "layout" section')

    args = {k: anim[k] for k in args if k in anim}
    project['layout'] = dict(args, datatype=layout_cl)
