import functools
try:
    import numpy
    numpy_array = numpy.array

except:
    numpy = None
    numpy_array = ()
