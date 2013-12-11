# greenthink-library (c) 2013 Ian Dennis Miller

SHELL=/bin/bash
WWWROOT=/var/www/greenthink-library
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests -c nose.cfg
SERVER_PLIST=com.gthnk.server.plist
LIBRARIAN_PLIST=com.gthnk.librarian.plist
DASHBOARD_PLIST=com.gthnk.dashboard.plist

clean:
	rm -rf build dist *.egg-info *.pyc

install: www launch
	mkdir -p /var/lib/greenthink-library
	mkdir -p ~/.gt
	python setup.py install
	cp etc/production.conf ~/.gt/greenthink.conf

www:
	rsync -a www/ $(WWWROOT)
	rsync -a GT/static/ $(WWWROOT)/static

launch:
	@echo "Installing launch agent to ~/Library/LaunchAgents"

	cp etc/$(SERVER_PLIST) ~/Library/LaunchAgents
	-launchctl unload ~/Library/LaunchAgents/$(SERVER_PLIST)
	launchctl load ~/Library/LaunchAgents/$(SERVER_PLIST)

	cp etc/$(LIBRARIAN_PLIST) ~/Library/LaunchAgents
	-launchctl unload ~/Library/LaunchAgents/$(LIBRARIAN_PLIST)
	launchctl load ~/Library/LaunchAgents/$(LIBRARIAN_PLIST)

	cp etc/$(DASHBOARD_PLIST) ~/Library/LaunchAgents
	-launchctl unload ~/Library/LaunchAgents/$(DASHBOARD_PLIST)
	launchctl load ~/Library/LaunchAgents/$(DASHBOARD_PLIST)

server:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py runserver

shell:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py shell

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\n; date; $(TEST_CMD); date' .

test:
	$(TEST_CMD)

lint:
	pylint GT

doc:
	rm -rf sphinx/source/auto && mkdir sphinx/source/auto
	sphinx-apidoc -o sphinx/source/auto/GT GT
	SETTINGS=$$PWD/etc/dev.conf sphinx-build -b html sphinx/source sphinx/build
	open sphinx/build/index.html

.PHONY: clean install test server watch lint www doc launch
