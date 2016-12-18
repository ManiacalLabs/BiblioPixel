from setuptools import setup
from setuptools.command.test import test as TestCommand
import bibliopixel


# from here: http://pytest.org/2.2.4/goodpractises.html
# this and RunBenchmark are near identical
# TODO: Find a way to combine these
class RunTests(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        #  import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)


class RunBenchmark(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['benchmarks']
        self.test_suite = True

    def run_tests(self):
        #  import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)


setup(
    name='BiblioPixel',
    version=bibliopixel.VERSION,
    description='BiblioPixel is a pure python library for manipulating a wide variety of LED strip based displays, both in strip and matrix form.',
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
        'test': RunTests,
        'benchmark': RunBenchmark
    }
)
