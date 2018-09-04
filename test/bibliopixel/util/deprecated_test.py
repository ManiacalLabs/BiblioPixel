"""
The test below cannot be run in process at the same time as any other test,
because once it has been imported, it turns off all deprecated feeatures for all
other tests (we can't just use a switch later because we don't know what got
imported with the deprecated flag set to at 'fail').

This makes a lot of tests fail, so so it is turned off by default with test flag
DEPRECATION_TESTS.  Once we move close to 4.0, and no longer rely on deprecated
features, we can get rid of that flag.

When run separately with the flag turned on, using

    DEPRECATION_TESTS=true pytest test -k deprecated

this test shows that we can at least load all but four modules.
"""

import unittest
from .. import all_test, mark_tests

if mark_tests.DEPRECATION_TESTS:
    from bibliopixel.util import deprecated
    deprecated.ACTION = 'fail'

BP_BLACKLIST = all_test.BP_BLACKLIST + [
    'bibliopixel.main.commands',
    'bibliopixel.main.demo',
    'bibliopixel.main.demo_table',
    'bibliopixel.main.main',
]


class DeprecatedTest(unittest.TestCase):
    @mark_tests.deprecation_tests
    def test_bp(self):
        all_test.TestAll._test(
            self, all_test.BP_ROOT, all_test.BP_NAME, BP_BLACKLIST)
