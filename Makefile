clean:
	rm -rf backend/.pytype

typecheck:
	python3 -m pytype --config backend/pytype.config

lint:
	python3 -m pylint --rcfile=backend/.pylintrc backend

all_checks: clean typecheck lint

run:
	python3 -m backend

import:
	python3 -m backend --import_toponyms

push: all_checks
	git push
