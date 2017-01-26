if ! flake8 ; then
    exit 1
fi

if ! coverage run -m unittest discover test \*_test.py . ; then
    exit 1
fi

coverage report
if ! coverage html ; then
    echo
    echo "ERROR: Failed coverage levels"
    open htmlcov/index.html
    exit 1
fi
