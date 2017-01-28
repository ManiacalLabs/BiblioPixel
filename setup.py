from setuptools import setup
from setuptools.command.test import test as TestCommand
import bibliopixel, sys


# From here: http://pytest.org/2.2.4/goodpractises.html
class RunTests(TestCommand):
    DIRECTORY = 'test'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.DIRECTORY]
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        if errno:
            raise SystemExit(errno)


class RunBenchmark(RunTests):
    DIRECTORY = 'benchmark'


class RunCoverage(RunTests):
    def run_tests(self):
        import coverage
        cov = coverage.Coverage(config_file=True)

        cov.start()
        super().run_tests()
        cov.stop()

        cov.report(file=sys.stdout)
        coverage = cov.html_report(directory='htmlcov')
        fail_under = cov.get_option('report:fail_under')
        if coverage < fail_under:
            print('ERROR: coverage %.2f%% was less than fail_under=%s%%' % (
                  coverage, fail_under))
            raise SystemExit(1)


setup(
    name='BiblioPixel',
    version=bibliopixel.VERSION,
    description=(
        'BiblioPixel is a pure python library for manipulating a wide variety '
        'of LED strip based displays, both in strip and matrix form.'),
    author='Adam Haile',
    author_email='adam@maniacallabs.com',
    url='http://github.com/maniacallabs/bibliopixel/',
    license='MIT',
    packages=['bibliopixel', 'bibliopixel.drivers'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=['pytest'],
    cmdclass={
        'benchmark': RunBenchmark,
        'coverage': RunCoverage,
        'test': RunTests,
    }
)
