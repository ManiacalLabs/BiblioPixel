#!/bin/bash

# delete ./api/ dir if exists
rm -rf ./api/ || true

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
