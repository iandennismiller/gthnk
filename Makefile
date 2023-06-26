# gthnk

help:
	@echo The following makefile targets are available:
	@echo
	@grep -e '^\w\S\+\:' Makefile | sed 's/://g' | cut -d ' ' -f 1
	@echo "### Docker"
	@grep -e '^\w\S\+\:' src/docker.mk | sed 's/://g' | cut -d ' ' -f 1
	@echo "### Dev"
	@grep -e '^\w\S\+\:' src/dev.mk | sed 's/://g' | cut -d ' ' -f 1
	@echo

install:
	pip install -U pip
	pip install -e ./src[server]

server:
	GTHNK_CONFIG=$$PWD/.env \
	FLASK_ENV=development \
	FLASK_RUN_PORT=1620 \
	FLASK_APP=src/gthnk_web/app \
		flask run

-include src/docker.mk
-include src/dev.mk
