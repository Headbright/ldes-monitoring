.PHONY: dev lint

DEPENDENCIES := $(shell test -f docker-compose-dependencies.yaml && yq ".services | length != 0" < docker-compose-dependencies.yaml)
# define standard colors
BLUE := $(shell tput -Txterm setaf 6)
YELLOW := $(shell tput -Txterm setaf 3)

RESET := $(shell tput -Txterm sgr0)

export DOCKER_BUILDKIT = 1


dev:
	. ./dev-config && python3 -m exporter

lint:
	@black .