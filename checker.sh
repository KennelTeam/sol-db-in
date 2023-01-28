venv/bin/python3 -m pytype --config backend/pytype.config
result1=$?

if [ $result1 -ne 0 ]; then
    echo "Typing checks failed!"
    exit 1;
fi

venv/bin/python3 -m pylint --rcfile=backend/.pylintrc backend
result2=$?

if [ $result2 -ne 0 ]; then
    echo "Linter checks failed!"
    exit 1
fi
echo "Successfully passed all checks!"
exit 0

