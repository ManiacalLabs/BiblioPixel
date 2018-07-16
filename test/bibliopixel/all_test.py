import os, unittest
from . import_all import import_all

BLACKLIST = ['bibliopixel.drivers.PiWS281X']
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

import BiblioPixelAnimations
BPA_ROOT = os.path.dirname(os.path.dirname(BiblioPixelAnimations.__file__))
BPA_BLACKLIST = [
    'BiblioPixelAnimations.cube.spectrum',
    'BiblioPixelAnimations.cube.spectrum.system_eq',
    'BiblioPixelAnimations.matrix.ScreenGrab',
    'BiblioPixelAnimations.matrix.kimotion',
    'BiblioPixelAnimations.matrix.opencv_video',
    'BiblioPixelAnimations.matrix.spectrum',
    'BiblioPixelAnimations.matrix.spectrum.system_eq',
    'BiblioPixelAnimations.receivers.GenericNetworkReceiver',
]


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        _, failures = import_all(
            PROJECT_ROOT, 'bibliopixel', BLACKLIST)
        self.assertEqual(failures, [])


class ImportBPATest(unittest.TestCase):
    maxDiff = 100000

    def test_all(self):
        _, failures = import_all(
            BPA_ROOT, 'BiblioPixelAnimations', BPA_BLACKLIST)
        self.assertEqual(failures, [])
