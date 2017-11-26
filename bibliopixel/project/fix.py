from . import construct, merge

DEFAULT_DRIVERS = [construct.to_type('simpixel')]


def fix_before_recursion(project):
    try:
        animation = construct.to_type_constructor(project['animation'])
        fix = animation['datatype'].PROJECT
    except:
        pass
    else:
        project = merge.merge(fix, project)

    driver = construct.to_type(project.pop('driver', {}))
    drivers = [construct.to_type(d) for d in project.get('drivers', [])]
    if driver:
        if drivers:
            drivers = [dict(driver, **d) for d in drivers]
        else:
            drivers = [driver]

    project['drivers'] = drivers or DEFAULT_DRIVERS
    return project


def fix_after_recursion(project):
    animation = project.get('run_animation', {}).get('animation')
    if not animation:
        raise ValueError('Missing "animation" section')

    datatype = animation.get('datatype')
    if not datatype:
        raise ValueError('Missing "datatype" in "animation" section')

    if not project.get('layout'):
        # Try to fill in the layout if it's missing.
        try:
            args = datatype.LAYOUT_ARGS
            layout_cl = datatype.LAYOUT_CLASS
        except:
            raise ValueError('Missing "layout" section')

        args = {k: animation[k] for k in args if k in animation}
        layout = dict(args, datatype=layout_cl)
        project['layout'] = layout

    elif not project['layout'].get('datatype'):
        raise ValueError('Missing "datatype" in "layout" section')

    return project
