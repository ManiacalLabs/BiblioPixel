# This has to be called with source create-virtualenv.sh to get the
# new-env and delete-env aliases

set -Eexo pipefail

function is_callable() {
    T=$(type -t $1)
    [[ $T == function || $T == alias || $T == file ]]
}

if is_callable new-env ; then
    echo "ONE"
    delete-env bp-release-test
    echo "TWO"
    new-env bp-release-test
fi

echo "THREE"
python setup.py install
echo "FOUR"
source scripts/developer_install
