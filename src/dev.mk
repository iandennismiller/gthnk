# gthnk

-include ./src/test-one.mk

requirements:
	pip install -U pip
	pip install -e ./src[dev]

clean:
	rm -rf src/*.egg-info src/build src/dist
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '.DS_Store' -delete

test-one:
	pytest -k $(TEST_ONE) ./src

test:
	pytest --cov=gthnk ./src
	mypy --check-untyped-defs --ignore-missing-imports ./src/gthnk ./src/gthnk_web
	pylint --disable C0114,R0913 ./src/gthnk
	pylint --disable C0114,R0913 ./src/gthnk_web

docs:
	rm -rf var/sphinx
	pip install -r docs/requirements.txt
	sphinx-build -b html docs var/sphinx

release: clean
	cd src && python setup.py sdist bdist_wheel
	twine check src/dist/*

upload:
	twine upload --config-file ~/.pypirc src/dist/*

.PHONY: docs
