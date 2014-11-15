# greenthink-library (c) 2013 Ian Dennis Miller

SHELL=/bin/bash
WWWROOT=/var/www/greenthink-library
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests -c tests/nose/test.cfg

clean:
	rm -rf build dist *.egg-info *.pyc

install: www launch
	mkdir -p /var/lib/greenthink-library
	mkdir -p ~/.gt
	python setup.py install
	cp etc/production.conf ~/.gt/greenthink.conf

www:
	rsync -a www/ $(WWWROOT)
	rsync -a Gthnk/static/ $(WWWROOT)/static

launchd:
	@echo "Installing launchd agent to ~/Library/LaunchAgents"

	cp etc/launchd/* ~/Library/LaunchAgents

	-launchctl unload ~/Library/LaunchAgents/com.gthnk.server.plist
	launchctl load ~/Library/LaunchAgents/com.gthnk.server.plist

	-launchctl unload ~/Library/LaunchAgents/com.gthnk.librarian.plist
	launchctl load ~/Library/LaunchAgents/com.gthnk.librarian.plist

	-launchctl unload ~/Library/LaunchAgents/com.gthnk.dashboard.plist
	launchctl load ~/Library/LaunchAgents/com.gthnk.dashboard.plist

server:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py runserver

shell:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py shell

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\n; date; $(TEST_CMD); date' .

test:
	$(TEST_CMD)

lint:
	pylint Gthnk

doc:
	rm -rf docs/source/auto
	mkdir -p docs/source/auto/$(MOD_NAME)
	sphinx-apidoc -o docs/source/auto/$(MOD_NAME) $(MOD_NAME)
	SETTINGS=$$PWD/etc/dev.conf sphinx-build -b html docs/source docs/build
	SETTINGS=$$PWD/etc/dev.conf sphinx-build -b text docs/source docs/build
	open docs/build/index.html

.PHONY: clean install test server watch lint www doc launch
