from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

INSTALLATION_ERROR = """INSTALLATION ERROR!

BiblioPixel v3 requires Python 3.4+ but
you are using version {0.major}.{0.minor}.{0.micro}

If you absolutely require using Python 2,
please install BiblioPixel v2.x using:

    > pip install "bibliopixel<3.0"

However we highly recommend using the latest BiblioPixel
(v3+) with Python 3.4+.
"""


if sys.version_info.major != 3:
    print(INSTALLATION_ERROR.format(sys.version_info))
    sys.exit(1)


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


def _get_version():
    from os.path import abspath, dirname, join
    filename = join(dirname(abspath(__file__)), 'bibliopixel', 'VERSION')
    return open(filename).read().strip()


VERSION = _get_version()

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

setup(
    name='BiblioPixel',
    version=VERSION,
    description=(
        'BiblioPixel is a pure python library for manipulating a wide variety '
        'of LED strip based displays, both in strip and matrix form.'),
    author='Adam Haile',
    author_email='adam@maniacallabs.com',
    url='http://github.com/maniacallabs/bibliopixel/',
    license='MIT',
    packages=find_packages(exclude=['test']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=['pytest'],
    cmdclass={
        'benchmark': RunBenchmark,
        'coverage': RunCoverage,
        'test': RunTests,
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bibliopixel = bibliopixel.main.main:main'
        ]
    },
    install_requires=REQUIRED
)
