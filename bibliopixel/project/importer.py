import loady
from . types import make
from . types.defaults import FIELD_TYPES
from distutils.version import LooseVersion


MINIMUM_VERSIONS = {'serial': '2.7'}

INSTALL_NAMES = {
    'BiblioPixelAnimations': 'BiblioPixelAnimations',
    'flask': 'flask',
    'noise': 'noise',
    'serial': 'pyserial',
}

VERSION_MESSAGE = """
You have version %s of module '%s' but you need version %s.

Please upgrade at the command line with:

    $ pip install %s --upgrade

"""

MISSING_MESSAGE = """
You are missing module '%s'.

Please install it at the command line with:

    $ pip install %s

"""


def validate_typename(typename):
    root_module = typename.split('.')[0]
    min_version = MINIMUM_VERSIONS.get(root_module)
    if not min_version:
        return

    version = __import__(root_module).VERSION
    if LooseVersion(version) >= LooseVersion(min_version):
        return

    install_name = INSTALL_NAMES.get(root_module, root_module)
    raise ValueError(VERSION_MESSAGE % (
        root_module, version, min_version, install_name))


def import_symbol(typename):
    try:
        result = loady.code.load(typename)
        validate_typename(typename)
        return result
    except ImportError as e:
        root_module = typename.split('.')[0]
        install_name = INSTALL_NAMES.get(root_module)
        if install_name:
            try:
                __import__(root_module)
            except ImportError:
                msg = MISSING_MESSAGE % (root_module, install_name)
                e.msg = msg + e.msg
        raise


def make_object(*args, typename, field_types=None, **kwds):
    """Make an object from a symbol."""
    symbol = import_symbol(typename)
    if hasattr(symbol, 'FIELD_TYPES'):
        field_types = symbol.FIELD_TYPES

    kwds = make.component(kwds, field_types or FIELD_TYPES)
    return symbol(*args, **kwds)
