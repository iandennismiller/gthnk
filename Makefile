# gthnk (c) Ian Dennis Miller

###
# To set up a fresh dev environment:
# make requirements develop db test-import server
###

install:
	cd src && python setup.py install

requirements:
	pip install -r requirements.txt

develop:
	pip install -r usr/dev/requirements.txt

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
	# twine upload --config-file ~/.pypirc dist/*

###
# Docker

USERNAME=gthnk
PASSWORD=gthnk
CONTAINER_EXEC=docker exec -it gthnk-server sudo -i -u gthnk

docker-compose:
	docker-compose -f src/docker/docker-compose.yaml up -d

docker-compose-down:
	docker-compose -f src/docker/docker-compose.yaml down

docker-run:
	docker run \
		-it \
		--rm \
		--name gthnk-server \
		-p 1620:1620 \
		-e TZ=America/Toronto \
		-v ~/.gthnk:/home/gthnk/.gthnk \
		iandennismiller/gthnk

docker-build: clean
	docker build -t iandennismiller/gthnk:latest .

docker-push:
	docker push iandennismiller/gthnk

docker-config:
	$(CONTAINER_EXEC) gthnk-config-init.sh /home/gthnk/.gthnk/gthnk.conf

docker-db:
	$(CONTAINER_EXEC) gthnk-db-init.sh

docker-user-add:
	$(CONTAINER_EXEC) gthnk-user-add.sh $(USERNAME) $(PASSWORD)

docker-user-del:
	$(CONTAINER_EXEC) gthnk-user-del.sh $(USERNAME)

docker-rotate:
	$(CONTAINER_EXEC) gthnk-rotate.sh

docker-shell:
	docker exec -it gthnk-server bash

.PHONY: clean install test server watch lint docs all single release homebrew develop coverage
