from . import aliases, importer


def construct(*args, datatype, typename=None, **kwds):
    """
    Construct an object from a type constructor.

    A type constructor is a dictionary which has a field "datatype" which has
    a callable method to construct a class, and a field "typename" which is the
    Python path of the function or class in "datatype".
    """
    return datatype(*args, **kwds)


def construct_reserved(*args, name=None, data=None, **desc):
    """Construct and add in the two reserved fields name and data"""
    result = construct(*args, **desc)
    result.name, result.data = name, data

    return result


def to_type(d):
    return {'typename': d} if isinstance(d, str) else d


def to_type_constructor(value, python_path=None):
    """"
    Tries to convert a value to a type constructor.

    If value is a string, then it used as the "typename" field.

    If the "typename" field exists, the symbol for that name is imported and
    added to the type constructor as a field "datatype".

    Throws:
         ImportError -- if "typename" is set but cannot be imported
         ValueError -- if "typename" is malformed
    """
    if not value:
        return value

    value = to_type(value)
    typename = value.get('typename')
    if typename:
        value['datatype'] = importer.import_symbol(
            aliases.resolve(typename), python_path=python_path)

    return value
