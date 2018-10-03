function is_callable() {
    T=$(type -t $1)
    [[ $T == function || $T == alias || $T == file ]]
}

RELEASE_TEST=$(pwd)/scripts/release_test/release_test

if [[ "$1" ]] ; then
    TEST_DIRECTORY="$1"
else
    TEST_DIRECTORY=/tmp
fi

if is_callable new-env ; then
    delete-env bp-release-test
    new-env bp-release-test
fi

python setup.py install
source scripts/developer_install

pushd $TEST_DIRECTORY >/dev/null
$RELEASE_TEST
popd >/dev/null

if is_callable delete-env ; then
    delete-env bp-release-test
fi
