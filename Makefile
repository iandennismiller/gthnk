# gthnk (c) Ian Dennis Miller

help:
	@echo The following makefile targets are available:
	@echo
	@grep -e '^\w\S\+\:' Makefile | sed 's/://g' | cut -d ' ' -f 1

install:
	pip install -U pip
	pip install -e ./src

install-server:
	pip install -U pip
	pip install -e ./src[server]

dev:
	pip install -e ./src[dev]

server:
	export SETTINGS=$$PWD/.env && \
	FLASK_ENV=development \
	FLASK_RUN_PORT=1620 \
	FLASK_APP=src/gthnk_server/server \
	flask run

shell:
	export SETTINGS=$$PWD/.env && \
		gthnk-manager shell

clean:
	rm -rf src/*.egg-info src/build src/dist
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

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
