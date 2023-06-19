# gthnk

USERNAME=gthnk
PASSWORD=gthnk
CONTAINER_EXEC=docker exec -it gthnk-server sudo -i -u gthnk

docker-compose:
	docker-compose -f docker-compose.yaml up -d

docker-compose-down:
	docker-compose -f docker-compose.yaml down

docker-run:
	docker run \
		-it \
		--rm \
		--name gthnk-server \
		-p 1620:1620 \
		-e TZ=America/Toronto \
		-v ~/.gthnk:/home/gthnk/.gthnk \
		iandennismiller/gthnk

docker-build: clean
	docker build -t iandennismiller/gthnk:latest .

docker-push:
	docker push iandennismiller/gthnk
