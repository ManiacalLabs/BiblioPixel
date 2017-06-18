PERMISSION_ERROR = """Cannot access SPI device.
Please see

    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

CANT_FIND_ERROR = """Cannot find SPI device.
Please see

    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

CANT_IMPORT_PERIPHERY_ERROR = """
Unable to import periphery. Please install:
    pip install python-periphery

Please see
    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

BAD_FORMAT_ERROR = """
When using py-spidev, `dev` must be in the format /dev/spidev*.*
Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup
"""

CANT_IMPORT_SPIDEV_ERROR = """
Unable to import spidev. Please install:

    pip install spidev
"""
