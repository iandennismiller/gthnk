# gthnk (c) Ian Dennis Miller

install:
	pip install -U pip
	pip install -r src/requirements.txt
	pip install -e ./src

develop:
	pip install -r src/requirements-dev.txt

clean:
	rm -rf src/*.egg-info src/build src/dist
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -f .coverage coverage.xml

test:
	pytest ./src

docs:
	rm -rf build/sphinx
	pip install -r docs/requirements.txt
	SETTINGS=$$PWD/usr/conf/testing.conf sphinx-build -b html docs build/sphinx

release:
	cd src && python setup.py sdist bdist_wheel
	twine upload --config-file ~/.pypirc src/dist/*

# server:
# 	export SETTINGS=$$PWD/usr/conf/dev.conf && \
# 	cd src/gthnk_server && \
# 		FLASK_ENV=development \
# 		FLASK_RUN_PORT=1620 \
# 		FLASK_APP=server.py \
# 		flask run

# shell:
# 	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk shell

# db:
# 	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk init_db
# 	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk user_add --username "gthnk" --password "gthnk"

# dropdb:
# 	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk drop_db

# upgradedb:
# 	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk db upgrade

# migratedb:
# 	SETTINGS=$$PWD/usr/conf/dev.conf src/scripts/gthnk db migrate

# coverage:
# 	SETTINGS=$$PWD/usr/conf/testing.conf nosetests --with-xcoverage \
# 		--cover-package=src/gthnk --cover-tests -c usr/nose/test.cfg

# lint:
# 	pylint src/gthnk

.PHONY: clean install test server watch lint docs all single release homebrew develop coverage
