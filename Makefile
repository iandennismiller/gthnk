# gthnk (c) 2014-2016 Ian Dennis Miller

PROJECT_NAME=gthnk
MOD_NAME=gthnk
SHELL=/bin/bash
WWWROOT=/var/www/gthnk
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests

all: install
	@echo Done

install:
	python setup.py install

clean:
	rm -rf build dist *.egg-info
	find . -name "*.pyc" -exec rm -rf {} \;

server:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py runserver

shell:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py shell

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\n; date; $(TEST_CMD) -c tests/nose/test-single.cfg; date' .

test:
	$(TEST_CMD) -c gthnk/tests/nose/test.cfg

xunit:
	$(TEST_CMD) --with-xunit -c tests/nose/test.cfg

single:
	$(TEST_CMD) -c tests/nose/test-single.cfg 2>&1 | tee -a ./makesingle.log

db:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py init_db
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py populate_db

lint:
	pylint gthnk

upgradedb:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py db upgrade

migratedb:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py db migrate

docs:
	rm -rf var/sphinx/build
	sphinx-build -b html docs var/sphinx/build

.PHONY: clean install test server watch lint docs all single
