def unknown(items, name, value):
    if items:
        msg = ', '.join('"%s"' % s for s in sorted(items))
        s = '' if len(items) == 1 else 's'
        raise ValueError('Unknown %s%s for %s: %s' % (name, s, value, msg))


def unknown_attributes(items, name, value):
    value = '%s %s' % (name, value.__class__.__name__)
    unknown(items, 'attribute', value)
