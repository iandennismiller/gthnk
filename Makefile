# gthnk (c) 2014-2017 Ian Dennis Miller

SHELL=/bin/bash
PROJECT_NAME=gthnk
MOD_NAME=gthnk
WATCHMEDO_PATH=$$(which watchmedo)
NOSETESTS_PATH=$$(which nosetests)
TEST_CMD=SETTINGS=$$PWD/etc/conf/testing.conf $(NOSETESTS_PATH) $(MOD_NAME)

install:
	python setup.py install

requirements:
	pip install -r requirements.txt

dev:
	pip install -r .requirements-dev.txt

clean:
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

server:
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py runserver

server-win:
	set SETTINGS=%cd%\etc\conf\dev-win.conf
	python bin\manage.py runserver

db-win:
	set SETTINGS=%cd%\etc\conf\dev-win.conf
	python bin\manage.py init_db
	python bin\manage.py user_add --email "guest@example.com" --password "guest"
	python bin\manage.py user_add --email "admin@example.com" --password "aaa" --admin

shell:
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py shell

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\nSTART; date; $(TEST_CMD) -c etc/nose/test-single.cfg; date' .

test:
	$(TEST_CMD) -c etc/nose/test.cfg

xunit:
	$(TEST_CMD) --with-xunit -c etc/nose/test.cfg

single:
	$(TEST_CMD) -c etc/nose/test-single.cfg

db:
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py init_db
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py populate_db

lint:
	pylint gthnk

upgradedb:
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py db upgrade

migratedb:
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py db migrate

docs:
	rm -rf build/sphinx
	SETTINGS=$$PWD/etc/conf/testing.conf sphinx-build -b html docs build/sphinx

release:
	python setup.py sdist upload

# create a homebrew install script
homebrew:
	bin/poet-homebrew.sh
	cp /tmp/gthnk.rb integrations/homebrew/gthnk.rb

.PHONY: clean install test server watch lint docs all single release homebrew
