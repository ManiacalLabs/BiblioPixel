#!/bin/bash

scripts/extract_bp_help doc/The-bp-Command.rst
pushd ./doc/

# delete ./api/ dir if exists
rm -rf ./api || true
sphinx-apidoc -o api ../bibliopixel/ ../bibliopixel/main/
make html
popd
