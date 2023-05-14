# gthnk (c) Ian Dennis Miller

###
# To set up a fresh dev environment:
# make requirements develop db test-import server
###

install:
	cd src && python setup.py install

requirements:
	pip install -r src/requirements.txt

develop:
	pip install -r src/requirements-dev.txt

clean:
	rm -rf build dist *.egg-info src/*.egg-info src/build src/dist
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -f .coverage coverage.xml

server:
	export SETTINGS=$$PWD/usr/conf/dev.conf && \
	cd src/gthnk && \
		FLASK_ENV=development \
		FLASK_RUN_PORT=1620 \
		FLASK_APP=server.py \
		flask run

shell:
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk shell

test: clean
	SETTINGS=$$PWD/usr/conf/testing.conf python -m tests.runner

test-import:
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk import_archive -d tests/data/

db:
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk init_db
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk user_add --username "gthnk" --password "gthnk"

dropdb:
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk drop_db

upgradedb:
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk db upgrade

migratedb:
	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk db migrate

docs:
	rm -rf build/sphinx
	pip install -r docs/requirements.txt
	SETTINGS=$$PWD/usr/conf/testing.conf sphinx-build -b html docs build/sphinx

coverage:
	SETTINGS=$$PWD/usr/conf/testing.conf nosetests --with-xcoverage \
		--cover-package=src/gthnk --cover-tests -c usr/nose/test.cfg

lint:
	pylint src/gthnk

release:
	cd src && python setup.py sdist bdist_wheel
	twine upload --config-file ~/.pypirc src/dist/*


.PHONY: clean install test server watch lint docs all single release homebrew develop coverage
