# gthnk

DOCKER_CMD=docker run \
	-it \
	--rm \
	--name gthnk \
	-p 1620:1620 \
	-e TZ=America/Toronto \
	-v ~/Work/gthnk/var/gthnk:/opt/gthnk/var \
	iandennismiller/gthnk:0.8

docker-shell:
	cd src && $(DOCKER_CMD) /bin/bash

docker-server:
	cd src && $(DOCKER_CMD)

docker-build: clean
	cd src && docker build -t iandennismiller/gthnk:0.8 .

docker-push:
	cd src && docker buildx build --platform linux/amd64,linux/arm64 -t iandennismiller/gthnk:0.8 --push .
