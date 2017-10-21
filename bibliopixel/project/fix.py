from . import importer


def to_type(d):
    return {'typename': d} if isinstance(d, str) else d


DEFAULT_DRIVERS = [to_type('simpixel')]


def fix_drivers(project):
    driver = to_type(project.pop('driver', {}))
    drivers = [to_type(d) for d in project.get('drivers', [])]
    if driver:
        if drivers:
            drivers = [dict(driver, **d) for d in drivers]
        else:
            drivers = [driver]

    project['drivers'] = drivers or DEFAULT_DRIVERS

    return project


def fix_layout(project):
    # This needs to be called after resolution.
    if project.get('layout'):
        return project

    animation = project.get('animation')
    if animation:
        animation_type = animation['datatype']
        args = {k: animation[k] for k in animation_type.LAYOUT_ARGS
                if k in animation}
        project['layout'] = dict(args, datatype=animation_type.LAYOUT_CLASS)

    return project
