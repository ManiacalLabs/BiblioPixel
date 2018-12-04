import os
from .. project import aliases, importer
from .. util import class_name, data_file, log

CLASS_SECTIONS = 'layout', 'animation', 'driver'


def set_one(desc, name, value):
    """Set one section in a Project description"""
    old_value = desc.get(name)
    if old_value is None:
        raise KeyError('No section "%s"' % name)

    if value is None:
        value = type(old_value)()

    elif name in CLASS_SECTIONS:
        if isinstance(value, str):
            value = {'typename': aliases.resolve(value)}
        elif isinstance(value, type):
            value = {'typename': class_name.class_name(value)}
        elif not isinstance(value, dict):
            raise TypeError('Expected dict, str or type, got "%s"' % value)

        typename = value.get('typename')
        if typename:
            s = 's' if name == 'driver' else ''
            path = 'bibliopixel.' + name + s
            importer.import_symbol(typename, path)

    elif name == 'shape':
        if not isinstance(value, (list, int, tuple, str)):
            raise TypeError('Expected shape, got "%s"' % value)

    elif type(old_value) is not type(value):
        raise TypeError('Expected %s but got "%s" of type %s' %
                        (type(old_value), value, type(value)))

    desc[name] = value


def update(desc, other=None, **kwds):
    """Update sections in a Project description"""
    other = other and _as_dict(other) or {}
    for i in other, kwds:
        for k, v in i.items():
            if isinstance(v, dict):
                # Only for dicts, merge instead of overwriting
                old_v = desc[k]
                for k2, v2 in v.items():
                    if v2 is None:
                        old_v.pop(k2, None)
                    else:
                        old_v[k2] = v2
            else:
                set_one(desc, k, v)


def _as_dict(data):
    if isinstance(data, dict):
        return data

    as_dict = getattr(data, 'as_dict', None)
    if callable(as_dict):
        return as_dict()

    if isinstance(as_dict, dict):
        return as_dict

    desc = getattr(data, 'desc', None)
    if desc is not None:
        return _as_dict(desc)

    if isinstance(data, str):
        data = data_file.load_if(data)
        if isinstance(data, dict):
            return data

    raise TypeError('Expected dict but got value "%s"' % data)
