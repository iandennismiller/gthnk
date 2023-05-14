###
# Docker

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

docker-config:
	$(CONTAINER_EXEC) gthnk-config-init.sh /home/gthnk/.gthnk/gthnk.conf

docker-db:
	$(CONTAINER_EXEC) gthnk-db-init.sh

docker-user-add:
	$(CONTAINER_EXEC) gthnk-user-add.sh $(USERNAME) $(PASSWORD)

docker-user-del:
	$(CONTAINER_EXEC) gthnk-user-del.sh $(USERNAME)

docker-rotate:
	$(CONTAINER_EXEC) gthnk-rotate.sh

docker-shell:
	docker exec -it gthnk-server bash
