from enum import IntEnum


def resolve_enum(enum_type, value):
    try:
        return enum_type[value]  # It's a string.
    except:
        return enum_type(value)   # It's an int.
