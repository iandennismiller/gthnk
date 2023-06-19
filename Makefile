# gthnk

help:
	@echo The following makefile targets are available:
	@echo
	@grep -e '^\w\S\+\:' Makefile | sed 's/://g' | cut -d ' ' -f 1

install:
	pip install -U pip
	pip install -e ./src

install-server:
	pip install -U pip
	pip install -e ./src[server]

dev:
	pip install -U pip
	pip install -e ./src[dev]

server:
	export SETTINGS=$$PWD/.env && \
	FLASK_ENV=development \
	FLASK_RUN_PORT=1620 \
	FLASK_APP=src/gthnk_web/app \
	flask run

-include src/docker.mk
-include src/dev.mk
