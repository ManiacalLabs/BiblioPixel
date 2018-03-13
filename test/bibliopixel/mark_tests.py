import os, unittest

"""This module long_test provides a decorator, @long_test, that you can use to
mark tests which take a lot of wall clock time.

If the system environment variable SKIP_LONG_TESTS is set, tests decorated
with @long_test will not be run.
"""

SKIP_LONG_TESTS = os.getenv('SKIP_LONG_TESTS', '').lower().startswith('t')
RUN_ALLPIXEL_TESTS = os.getenv('RUN_ALLPIXEL_TESTS', '').lower().startswith('t')

long_test = unittest.skipIf(SKIP_LONG_TESTS, 'Long tests skipped.')
allpixel_test = unittest.skipIf(
    not RUN_ALLPIXEL_TESTS, 'AllPixel tests skipped.')
