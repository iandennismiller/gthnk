# gthnk

TEST_ONE=test_import_buffers

requirements:
	pip install -U pip
	pip install -e ./src[dev]

clean:
	rm -rf src/*.egg-info src/build src/dist
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

test-one:
	pytest -k $(TEST_ONE) ./src

test:
	pytest ./src
	mypy --check-untyped-defs ./src/gthnk
#	mypy ./src/gthnk_web

docs:
	rm -rf build/sphinx
	pip install -r docs/requirements.txt
	SETTINGS=$$PWD/usr/conf/testing.conf sphinx-build -b html docs build/sphinx

release:
	cd src && python setup.py sdist bdist_wheel
	twine upload --config-file ~/.pypirc src/dist/*
