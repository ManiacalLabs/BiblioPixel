#!/bin/bash
set -Eeuxo pipefail

# This script checks out a clean copy of BiblioPixel and BiblioPixelAnimations
# into the current directory.
#
# You must already have forked the BiblioPixel and BiblioPixelAnimations
# repositories on github.

if [ "$1" == "" ]; then
    echo "Missing username!"
    echo "USAGE: checkout.sh <git-username> [http]"
    return -1
fi

GITUSER=$1
CMD=${2:-git}

if [ $1 == http ]; then
    PREFIX='https://github.com/'
else
    PREFIX='git@github.com:'
fi

git clone $PREFIX$1/BiblioPixel
git clone $PREFIX$1/BiblioPixelAnimations

cd BiblioPixel
git remote add upstream ${PREFIX}ManiacalLabs/BiblioPixel.git
git remote add rec ${PREFIX}rec/BiblioPixel.git

cd ../BiblioPixelAnimations
git remote add upstream ${PREFIX}ManiacalLabs/BiblioPixelAnimations.git
git remote add rec ${PREFIX}rec/BiblioPixelAnimations.git

cd ..
