SHELL := /usr/bin/env bash

init:
	@scripts/init.sh

docker:
	@docker build -t exponea_api ./src || sudo !! \
 	&&  docker run --rm -it -p 5000:80 exponea_api || sudo !!

run:
	@docker-compose up || sudo !!

local:
	@python3 ./src/main.py

clean:
	@docker stop `(docker ps -a -q)` || true
	@docker rm `(docker ps -a -q)` || true
	@docker  rmi `(docker images -q)` -f

test:
	@scripts/test.sh

exec_docker:
	@scripts/exec_docker.sh
