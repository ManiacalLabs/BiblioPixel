#!/bin/bash

scripts/extract_bp_help doc/The-bp-Command.rst
pushd ./doc/

# delete ./api/ dir if exists
rm -rf ./api/ ./_build/ || true

sphinx-apidoc \
    -o api \
    ../bibliopixel/ \
    ../bibliopixel/main/ \
    ../bibliopixel/util/threads/ \
    ../bibliopixel/util/colors/arithmetic.py \
    ../bibliopixel/util/colors/conversions.py \
    ../bibliopixel/util/colors/classic.py \
    ../bibliopixel/util/colors/gamma.py \
    ../bibliopixel/util/colors/juce.py \
#

make html
popd
