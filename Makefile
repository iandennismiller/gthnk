# gthnk (c) 2014 Ian Dennis Miller

PROJECT_NAME=gthnk
MOD_NAME=Gthnk
SHELL=/bin/bash
WWWROOT=/var/www/gthnk
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests

install:
	python setup.py install

all: paths install launchd
	@echo Done

clean:
	rm -rf build dist *.egg-info *.pyc

conf:
	mkdir -p /var/lib/gthnk ~/.gthnk
	cp etc/production.conf ~/.gthnk/gthnk.conf

launchd:
	@echo "Installing launchd agents to ~/Library/LaunchAgents"
	cp etc/launchd/* ~/Library/LaunchAgents
	-launchctl stop com.gthnk.server
	-launchctl unload ~/Library/LaunchAgents/com.gthnk.server.plist \
		~/Library/LaunchAgents/com.gthnk.librarian.plist \
		~/Library/LaunchAgents/com.gthnk.dashboard.plist
	launchctl load ~/Library/LaunchAgents/com.gthnk.server.plist \
		~/Library/LaunchAgents/com.gthnk.librarian.plist \
		~/Library/LaunchAgents/com.gthnk.dashboard.plist

server:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py runserver

shell:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py shell

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\n; date; $(TEST_CMD) -c tests/nose/test-single.cfg; date' .

test:
	$(TEST_CMD) -c tests/nose/test.cfg

xunit:
	$(TEST_CMD) --with-xunit -c tests/nose/test.cfg

single:
	$(TEST_CMD) -c tests/nose/test-single.cfg 2>&1 | tee -a ./makesingle.log

db:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py init_db
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py populate_db

lint:
	pylint Gthnk

docs:
	rm -rf var/sphinx/build
	sphinx-build -b html docs var/sphinx/build

.PHONY: clean install test server watch lint docs launchd paths all single
