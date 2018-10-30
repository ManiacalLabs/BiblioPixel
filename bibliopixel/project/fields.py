from . types import (
    channel_order, color, colors, direction, duration, gamma, int_name, ledtype,
    spi_interface)


FIELD_TYPES = {
    'bgcolor': color,
    'c_order': channel_order,
    'channel_order': channel_order,
    'color': color,
    'color1': color,
    'color2': color,
    'colors': colors,
    'count': int_name,
    'direction': direction,
    'duration': duration,
    'func': int_name,
    'gamma': gamma,
    'i': int_name,
    'ledtype': ledtype,
    'num': int_name,
    'offColor': color,
    'onColor': color,
    'palette': colors,
    'spi_interface': spi_interface,
    'time': duration,
}


def type_converter(types):
    def converter(value):
        for key, maker in types.items():
            if key not in value:
                continue
            try:
                value[key] = maker.make(value[key])
            except Exception as e:
                e.args = ('For key=%s value=%s' % (
                    key, value[key]),) + e.args
                raise

        return value

    return converter


default_converter = type_converter(FIELD_TYPES)


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
