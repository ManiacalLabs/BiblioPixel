from setuptools import setup
import bibliopixel

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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
