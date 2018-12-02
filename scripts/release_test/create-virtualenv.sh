# This has to be called with source create-virtualenv.sh to get the
# new-env and delete-env aliases

set -Eexo pipefail

function is_callable() {
    T=$(type -t $1)
    [[ $T == function || $T == alias || $T == file ]]
}

if is_callable new-env ; then
    delete-env bp-release-test
    new-env bp-release-test
fi

python setup.py install
source scripts/developer_install
