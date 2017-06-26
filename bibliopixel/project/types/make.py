def field_value(field, value, types):
    if field not in types:
        return value

    try:
        return types[field].make(value)
    except Exception as e:
        e.args += ('for field %s and value %s' % (field, value), )
        raise


def component(comp, types):
    return {k: field_value(k, v, types) for k, v in comp.items()}


def project(proj, types):
    return {k: component(v, types) for k, v in proj.items()}
