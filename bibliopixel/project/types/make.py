def field_value(field, value, field_types):
    if not (field_types and field in field_types):
        return value

    try:
        return field_types[field].make(value)
    except Exception as e:
        e.args += ('for field %s and value %s' % (field, value), )
        raise


def component(comp, field_types):
    return {k: field_value(k, v, field_types) for k, v in comp.items()}


def project(proj, field_types):
    return {k: component(v, field_types) for k, v in proj.items()}
