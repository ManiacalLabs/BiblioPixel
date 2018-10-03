"""
This module provides decorator, @long_test, that you can use to mark tests
with various properties, and then turn them off or on with enviroment variables.
"""

import os
from unittest import skipIf


def _check(env):
    return os.getenv(env, '').lower().startswith('t')


SKIP_LONG_TESTS = _check('SKIP_LONG_TESTS')
RUN_ALLPIXEL_TESTS = _check('RUN_ALLPIXEL_TESTS')
FAILS_IN_TRAVIS = _check('TRAVIS')
DEPRECATION_TESTS = _check('DEPRECATION_TESTS')
FAILS_ON_WINDOWS = os.name == 'nt'

long_test = skipIf(SKIP_LONG_TESTS, 'Long tests skipped.')
allpixel_test = skipIf(not RUN_ALLPIXEL_TESTS, 'AllPixel tests skipped.')
fails_in_travis = skipIf(True or FAILS_IN_TRAVIS, 'Travis-flakey tests skipped')
fails_on_windows = skipIf(FAILS_ON_WINDOWS, 'Windows-flakey tests skipped')
deprecation_tests = skipIf(not DEPRECATION_TESTS, 'Tests of deprecation skipped')
