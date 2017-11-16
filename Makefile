# gthnk (c) 2014-2017 Ian Dennis Miller

SHELL=/bin/bash
PROJECT_NAME=gthnk
MOD_NAME=gthnk

install:
	python setup.py install

requirements:
	pip install -r requirements.txt

dev:
	pip install -r .requirements-dev.txt

clean:
ifeq ($(OS),Windows_NT)
	@echo "not yet implemented on windows"
else
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
endif

server:
ifeq ($(OS),Windows_NT)
	set SETTINGS=%cd%\etc\conf\dev-win.conf
	python bin\manage.py runserver
else
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py runserver
endif

shell:
ifeq ($(OS),Windows_NT)
	set SETTINGS=%cd%\etc\conf\dev-win.conf
	python bin\manage.py shell
else
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py shell
endif

test:
ifeq ($(OS),Windows_NT)
	set SETTINGS=%cd%\etc\conf\testing-win.conf
	nosetests $(MOD_NAME) -c etc\nose\test.cfg
else
	nosetests $(MOD_NAME) -c etc/nose/test.cfg
endif

single:
ifeq ($(OS),Windows_NT)
	nosetests $(MOD_NAME) -c etc\nose\test-single.cfg
else
	nosetests $(MOD_NAME) -c etc/nose/test-single.cfg
endif

db:
ifeq ($(OS),Windows_NT)
	set SETTINGS=%cd%\etc\conf\dev-win.conf
	python bin\manage.py init_db
	python bin\manage.py user_add --email "guest@example.com" --password "guest"
	python bin\manage.py user_add --email "admin@example.com" --password "aaa" --admin
else
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py init_db
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py user_add --email "guest@example.com" --password "guest"
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py user_add --email "admin@example.com" --password "aaa" --admin
endif

watch:
ifeq ($(OS),Windows_NT)
	@echo "not yet implemented on windows"
else
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\nSTART; date; \
		SETTINGS=$$PWD/etc/conf/testing.conf nosetests $(MOD_NAME) \
		-c etc/nose/test-single.cfg; date' .
endif

upgradedb:
ifeq ($(OS),Windows_NT)
	@echo "not yet implemented on windows"
else
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py db upgrade
endif

migratedb:
ifeq ($(OS),Windows_NT)
	@echo "not yet implemented on windows"
else
	SETTINGS=$$PWD/etc/conf/dev.conf bin/manage.py db migrate
endif

docs:
ifeq ($(OS),Windows_NT)
	@echo "not yet implemented on windows"
else
	rm -rf build/sphinx
	SETTINGS=$$PWD/etc/conf/testing.conf sphinx-build -b html docs build/sphinx
endif

lint:
	pylint gthnk

release:
	python setup.py sdist upload

# create a homebrew install script
homebrew:
ifeq ($(OS),Windows_NT)
	@echo "not yet implemented on windows"
else
	integration/homebrew/poet-homebrew.sh
	cp /tmp/gthnk.rb integrations/homebrew/gthnk.rb
endif

.PHONY: clean install test server watch lint docs all single release homebrew
