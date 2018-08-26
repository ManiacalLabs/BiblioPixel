import os
from unittest import skipIf

"""This module long_test provides a decorator, @long_test, that you can use to
mark tests which take a lot of wall clock time.

If the system environment variable SKIP_LONG_TESTS is set, tests decorated
with @long_test will not be run.
"""

SKIP_LONG_TESTS = os.getenv('SKIP_LONG_TESTS', '').lower().startswith('t')
RUN_ALLPIXEL_TESTS = os.getenv('RUN_ALLPIXEL_TESTS', '').lower().startswith('t')
FAILS_IN_TRAVIS = os.getenv('TRAVIS', '').lower().startswith('t')
FAILS_ON_WINDOWS = os.name == 'nt'

long_test = skipIf(SKIP_LONG_TESTS, 'Long tests skipped.')
allpixel_test = skipIf(not RUN_ALLPIXEL_TESTS, 'AllPixel tests skipped.')
fails_in_travis = skipIf(FAILS_IN_TRAVIS, 'Travis-flakey tests skipped')
fails_on_windows = skipIf(FAILS_ON_WINDOWS, 'Travis-flakey tests skipped')
