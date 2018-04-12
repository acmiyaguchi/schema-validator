.PHONY: build clean redis-cli run shell stop up test

help:
	@echo "Welcome to the mozschema\n"
	@echo "The list of commands for local development:\n"
	@echo "  build      Builds the docker images for the docker-compose setup"
	@echo "  clean      Stops and removes all docker containers"
	@echo "  redis-cli  Opens a Redis CLI"
	@echo "  shell      Opens a Bash shell"
	@echo "  up         Runs the whole stack, served under http://localhost:8000/\n"
	@echo "  stop       Stops the docker containers"
	@echo "  test       Run a simple integration test"

build:
	docker-compose build

clean: stop
	docker-compose rm -f

shell:
	docker-compose run web bash

redis-cli:
	docker-compose run redis redis-cli -h redis

stop:
	docker-compose down
	docker-compose stop

up:
	docker-compose up

test:
	bash run-compose-test.sh
