# gthnk (c) 2014 Ian Dennis Miller

SHELL=/bin/bash
WWWROOT=/var/www/gthnk
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests -c tests/nose/test.cfg

install:
	python setup.py install

all: paths install www launchd
	@echo Done

clean:
	rm -rf build dist *.egg-info *.pyc

paths:
	mkdir -p /var/lib/gthnk ~/.gthnk
	cp etc/production.conf ~/.gthnk/gthnk.conf

www:
	rsync -a www/ $(WWWROOT)
	rsync -a Gthnk/static/ $(WWWROOT)/static

launchd:
	@echo "Installing launchd agents to ~/Library/LaunchAgents"
	cp etc/launchd/* ~/Library/LaunchAgents
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
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\n; date; $(TEST_CMD); date' .

test:
	$(TEST_CMD)

db:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py init_db
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py populate_db

lint:
	pylint Gthnk

doc:
	rm -rf docs/source/auto
	mkdir -p docs/source/auto/$(MOD_NAME)
	sphinx-apidoc -o docs/source/auto/$(MOD_NAME) $(MOD_NAME)
	SETTINGS=$$PWD/etc/dev.conf sphinx-build -b html docs/source docs/build
	SETTINGS=$$PWD/etc/dev.conf sphinx-build -b text docs/source docs/build
	open docs/build/index.html

.PHONY: clean install test server watch lint www doc launchd paths all
