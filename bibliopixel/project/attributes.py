def check(kwds, name):
    if kwds:
        msg = ', '.join('"%s"' % s for s in sorted(kwds))
        s = '' if len(kwds) == 1 else 's'
        raise ValueError('Unknown attribute%s for %s: %s' % (s, name, msg))


def set_reserved(value, section, name=None, data=None, **kwds):
    check(kwds, '%s %s' % (section, value.__class__.__name__))
    value.name = name
    value.data = data
