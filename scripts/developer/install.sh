#!/bin/bash

#
# Install all the packages necessary for BiblioPixel development into
# the current virtualenv, and then install BiblioPixel and BiblioPixelAnimations
# into the current virtualenv as "develop" so that changes to the code will be
# immediately reflected when you run `bp`.
#

# The right package is's python-rtmidi, not rtmidi, so uninstall that
# if it was accidentally installed - the two packages conflict
pip uninstall -q rtmidi

pip install -r requirements.txt
pip install -r test_requirements.txt
pip install -r doc/requirements.txt
pip install -r scripts/developer/requirements.txt

python setup.py develop

# TODO: these next two lines are janky - they are required because of a bug in
# BiblioPixelAnimations's setup.py, but they won't work on every system.  We
# should fix that bug and then remove the last two lines

cd ../BiblioPixelAnimations
python setup.py develop
cd ../BiblioPixel
