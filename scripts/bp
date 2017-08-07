#!/usr/bin/env python3

import platform

MINIMUM_VERSION = '3.4.0'

if platform.python_version() < MINIMUM_VERSION:
    raise EnvironmentError(
        'BiblioPixel needs Python %s or later: your Python version is %s' % (
            MINIMUM_VERSION, platform.python_version()))

from bibliopixel.main import main

if __name__ == '__main__':
    main.main()
