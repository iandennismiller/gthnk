# gthnk (c) Ian Dennis Miller

###
# To set up a fresh dev environment:
# make requirements develop db test-import server
###

SHELL=/bin/bash
PROJECT_NAME=gthnk
MOD_NAME=gthnk

install:
	python setup.py install

requirements:
	pip install -r requirements.txt

develop:
	pip install -r .dev/requirements.txt

clean:
	rm -rf build dist *.egg-info src/*.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -f .coverage coverage.xml

server:
	mkdir -p var/log

	export SETTINGS=$$PWD/.dev/conf/dev.conf && \
	cd src/gthnk && \
		FLASK_ENV=development \
		FLASK_RUN_PORT=1620 \
		FLASK_APP=server.py \
		flask run

shell:
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk shell

test: clean
	SETTINGS=$$PWD/.dev/conf/testing.conf nosetests $(MOD_NAME) -c .dev/nose/test.cfg

test-import:
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk import_archive -d src/tests/data/

single:
	SETTINGS=$$PWD/.dev/conf/testing.conf nosetests $(MOD_NAME) -c .dev/nose/test-single.cfg

db:
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk init_db
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk user_add --username "gthnk" --password "gthnk"

dropdb:
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk drop_db

upgradedb:
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk db upgrade

migratedb:
	SETTINGS=$$PWD/.dev/conf/dev.conf bin/gthnk db migrate

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\nSTART; date; \
		SETTINGS=$$PWD/.dev/conf/testing.conf nosetests $(MOD_NAME) \
		-c .dev/nose/test-single.cfg; date' .

docs:
	rm -rf build/sphinx
	pip install -r docs/requirements.txt
	SETTINGS=$$PWD/.dev/conf/testing.conf sphinx-build -b html docs build/sphinx

coverage:
	SETTINGS=$$PWD/.dev/conf/testing.conf nosetests --with-xcoverage \
		--cover-package=$(MOD_NAME) --cover-tests -c .dev/nose/test.cfg

lint:
	pylint src/gthnk

release:
	python setup.py sdist bdist_wheel
	# twine upload --config-file ~/.pypirc dist/*

###
# Docker

CONTAINER=iandennismiller/gthnk
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
		$(CONTAINER)

docker-build:
	docker build -t $(CONTAINER):latest .

docker-push:
	docker push $(CONTAINER)

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
