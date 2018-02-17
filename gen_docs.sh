#!/bin/bash

scripts/extract_bp_help doc/bp-Command.md
pushd ./doc/

# delete ./_build/ dir if exists
rm -rf ./_build/ || true

make html
popd
