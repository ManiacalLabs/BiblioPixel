import math, threading, time
from . matrix import Matrix
from .. util import deprecated

if deprecated.allowed():  # pragma: no cover
    class POV(Matrix):
        def __init__(self, *args, **kwds):
            raise ValueError('layout.POV has been removed. Use animation.POV')

    LEDPOV = POV
