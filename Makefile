ARTIFACT_NAME="csesoc/showcse"
LISTEN_BIND="127.0.0.1:8000"
ENV_FILE="env.sh"
DOCKER_NAME="showcse"

build:
	docker build --rm -t $(ARTIFACT_NAME) .

push:
	docker push  $(ARTIFACT_NAME)

create:
	docker create --name $(DOCKER_NAME).mysql -e MYSQL_RANDOM_ROOT_PASSWORD=true --env-file=$(ENV_FILE) mysql
	docker create --name $(DOCKER_NAME) --env-file=$(ENV_FILE) --link $(DOCKER_NAME).mysql:mysql -p $(LISTEN_BIND):8080 $(ARTIFACT_NAME)

seed: start-mysql
	sleep 2
	docker run -it --rm --volumes-from=$(DOCKER_NAME) --env-file=$(ENV_FILE) --link $(DOCKER_NAME).mysql:mysql $(ARTIFACT_NAME) python3 run.py db upgrade

start-mysql:
	docker start $(DOCKER_NAME).mysql

start-main:
	docker start $(DOCKER_NAME)

start: start-mysql start-main

stop:
	docker stop -t 5 $(DOCKER_NAME) $(DOCKER_NAME).mysql

destroy: stop
	docker rm -v $(DOCKER_NAME)
	docker rm -v $(DOCKER_NAME).mysql
