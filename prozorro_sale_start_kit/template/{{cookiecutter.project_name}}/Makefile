PROJECT_NAME={{ cookiecutter.project_name }}
IMAGE ?= prozorro-sale-$(PROJECT_NAME):develop
IMAGE_TEST ?= prozorro-sale-$(PROJECT_NAME):develop-test
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short HEAD)
GIT_STAMP ?= $(shell git describe)
CHART_MUSEUM_URL ?= "https://helm.prozorro.sale/api/charts"

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20


.EXPORT_ALL_VARIABLES:

ifdef CI
  IMAGE_TARGET =
  TESTS_DEBUG_OPTS =
  REBUILD_IMAGES_FOR_TESTS =
else
  IMAGE_TARGET = --target=local
  TESTS_DEBUG_OPTS = -s --pdb-errors
  REBUILD_IMAGES_FOR_TESTS = docker-build
endif

# Common

all: help
start: run
clean: remove-compose

## Runs application development on docker. Builds, creates, starts containers for a service. | Common
run: docker-build
	@docker-compose up $(PROJECT_NAME)-local

## Stops application. Stops running container without removing them.
stop:
	@docker-compose stop

## Show logs
logs:
	@docker-compose logs -f $(PROJECT_NAME)-local

## Stop application and remove containers for a service.
remove-compose:
	@docker network prune -f
	@docker-compose down

## Runs command `bash` commands in docker container.
bash:
	@docker exec -it $(PROJECT_NAME) bash

## Builds docker image
docker-build:
	@docker build $(IMAGE_TARGET) --build-arg version=$(GIT_STAMP) \
		--build-arg twine_username=$(TWINE_USERNAME) \
		--build-arg twine_password=$(TWINE_PASSWORD) \
		-t $(IMAGE) .
	@docker build --target=test --build-arg version=$(GIT_STAMP) \
		--build-arg twine_username=$(TWINE_USERNAME) \
		--build-arg twine_password=$(TWINE_PASSWORD) \
		-t $(IMAGE_TEST) .

## Runs integration tests | Tests
test-integration: $(REBUILD_IMAGES_FOR_TESTS)
	@docker rm -f $(PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA) || true
	@docker-compose run --name $(PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA) $(PROJECT_NAME)-test-integration \
		pytest -v -q --cov-report= --cov=prozorro_sale test/integration/
	@docker cp $(PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA):/$(PROJECT_NAME)/.coverage .coverage.integration

## Runs unit tests
test-unit: $(REBUILD_IMAGES_FOR_TESTS)
	@docker rm -f $(PROJECT_NAME)-unit-$(CI_COMMIT_SHORT_SHA) || true
	@docker-compose run --name $(PROJECT_NAME)-unit-$(CI_COMMIT_SHORT_SHA) $(PROJECT_NAME)-test-unit \
	pytest -v -q --cov-report= --cov=prozorro_sale test/unit/
	@docker cp $(PROJECT_NAME)-unit-$(CI_COMMIT_SHORT_SHA):/$(PROJECT_NAME)/.coverage .coverage.unit

# Linters & tests | Linters

## Formats code with `flake8`.
lint: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-local flake8 /$(PROJECT_NAME)/

## Safety checks your installed dependencies for known security vulnerabilities.
safety: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-local safety check --full-report

## Bandit is a tool designed to find common security issues in Python code.
bandit: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-local bandit --exit-zero -r /$(PROJECT_NAME)/

## Checks types with `mypy`.
mypy: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-local mypy --config-file=/.mypy.ini /$(PROJECT_NAME)/

## Build helm | Release
helm-build:
	@helm package helm/prozorro-sale-$(PROJECT_NAME) --app-version=$(GIT_STAMP) --version=$(GIT_STAMP)

## Check helm
helm-lint:
	@helm lint helm/prozorro-sale-$(PROJECT_NAME)

## Publish helm
push-helm-package:
	@curl \
		--user $(CHART_MUSEUM_USER):$(CHART_MUSEUM_PASS) \
		--data-binary "@prozorro-sale-$(PROJECT_NAME)-$(GIT_STAMP).tgz" \
		$(CHART_MUSEUM_URL)

## Publish coverage report
publish-coverage:
	@docker rm -f $(CI_COMMIT_SHORT_SHA) || true
	@docker run -d --name $(CI_COMMIT_SHORT_SHA) $(IMAGE_TEST) sleep infinity
	@docker cp .coverage.unit $(CI_COMMIT_SHORT_SHA):/tmp/
	@docker cp .coverage.integration $(CI_COMMIT_SHORT_SHA):/tmp/
	@docker exec $(CI_COMMIT_SHORT_SHA) bash -c "cd /tmp && coverage combine && coverage report && coverage html -d cover-html"
	@docker cp $(CI_COMMIT_SHORT_SHA):/tmp/cover-html cover-html
	@docker rm -f $(CI_COMMIT_SHORT_SHA)


## Create tag
version:
	$(eval GIT_TAG ?= $(shell git describe --abbrev=0))
	$(eval VERSION ?= $(shell read -p "Version: " VERSION; echo $$VERSION))
	echo "Tagged release $(VERSION)\n" > Changelog-$(VERSION).txt
	git log --oneline --no-decorate --no-merges $(GIT_TAG)..HEAD >> Changelog-$(VERSION).txt
	git tag -a -e -F Changelog-$(VERSION).txt $(VERSION)


## Shows help. | Help
help:
	@echo ''
	@echo 'Usage:'
	@echo ''
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-_]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
		    if (index(lastLine, "|") != 0) { \
				stage = substr(lastLine, index(lastLine, "|") + 1); \
				printf "\n ${GRAY}%s: \n\n", stage;  \
			} \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			if (index(lastLine, "|") != 0) { \
				helpMessage = substr(helpMessage, 0, index(helpMessage, "|")-1); \
			} \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''