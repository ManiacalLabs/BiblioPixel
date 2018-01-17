import functools
from ...drivers.spi_interfaces import SPI_INTERFACES

USAGE = """
A spi_interface is represented by a string.

Possible values are """ + ', '.join(sorted(SPI_INTERFACES.__members__))


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(SPI_INTERFACES)
def _(c):
    return c


@make.register(str)
def _(c):
    return SPI_INTERFACES[c]
