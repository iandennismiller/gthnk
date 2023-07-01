# gthnk

GTHNK_VER=$(word 3, $(shell grep __version__ src/gthnk/__meta__.py))

DOCKER_CMD=docker run \
	-it \
	--rm \
	--name gthnk \
	-p 1620:1620 \
	-e TZ=America/Toronto \
	-v ~/Work/gthnk/var/gthnk:/opt/gthnk/var \
	iandennismiller/gthnk:$(GTHNK_VER)

docker-shell:
	cd src && $(DOCKER_CMD) /bin/bash

docker-server:
	cd src && $(DOCKER_CMD)

docker-build: clean
	cd src && docker build -t iandennismiller/gthnk:$(GTHNK_VER) .

docker-push:
	cd src && docker buildx build --platform linux/amd64,linux/arm64 -t iandennismiller/gthnk:$(GTHNK_VER) --push .
