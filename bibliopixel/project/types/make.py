from . import channel_order, color, duration, gamma, ledtype

_DEFAULT = {
    'channel_order': channel_order,
    'c_order': channel_order,
    'color': color,
    'duration': duration,
    'gamma': gamma,
    'ledtype': ledtype,
    'time': duration,
    'type': ledtype,
}


def field_value(field, value, types=None):
    if types is None:
        types = _DEFAULT

    if field not in types:
        return value

    try:
        return types[field].make(value)
    except Exception as e:
        e.args += ('for field %s and value %s' % (field, value), )
        raise


def component(comp, types=None):
    return {k: field_value(k, v, types) for k, v in comp.items()}


def project(proj, types=None):
    return {k: component(v, types) for k, v in proj.items()}
