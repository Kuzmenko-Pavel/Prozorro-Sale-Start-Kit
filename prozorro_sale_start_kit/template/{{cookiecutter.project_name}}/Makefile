PROJECT_NAME={{cookiecutter.project_name}}
IMAGE ?= prozorro-sale-$(PROJECT_NAME):develop
IMAGE_TEST ?= prozorro-sale-$(PROJECT_NAME):develop-test
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short HEAD)
GIT_STAMP ?= $(shell git describe || echo v0.1.0)
CHART_MUSEUM_URL ?= "https://helm.prozorro.sale/api/charts"
CI_PIPELINE_ID ?= 1
COMPOSE_PROJECT_NAME ?= $(PROJECT_NAME)-$(CI_PIPELINE_ID)

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20

ifeq ($(CI_COMMIT_REF_NAME), master)
	EGG_INFO = egg_info --tag-date
	HELM_STAMP =
else ifeq ($(shell echo ${CI_COMMIT_REF_NAME} | grep -o "^epic/"), epic/)
  	EGG_INFO = egg_info --tag-date --tag-build=DEV
  	HELM_STAMP = -epic
else
	EGG_INFO =
	HELM_STAMP =
endif

ifdef CI
  IMAGE_TARGET =
  TESTS_DEBUG_OPTS =
  REBUILD_IMAGES_FOR_TESTS =
else
  IMAGE_TARGET = --target=local
  TESTS_DEBUG_OPTS = -s --pdb-errors
  REBUILD_IMAGES_FOR_TESTS = docker-build
endif

.EXPORT_ALL_VARIABLES:

# Common

all: help
{%- if cookiecutter.use_docker == 'y' %}
start: run
clean: remove-compose

## Runs application development on docker. Builds, creates, starts containers for a service. | Common
run: docker-build
	@docker-compose up $(PROJECT_NAME)-local $(PROJECT_NAME)-databridge-local

## Stops application. Stops running container without removing them.
stop:
	@docker-compose stop

## Show logs
logs:
	@docker-compose logs -f $(PROJECT_NAME)-local

## Stop application and remove containers for a service.
remove-compose:
	@docker network ls -q -f name=$(PROJECT_NAME)* | xargs --no-run-if-empty docker network rm
	@docker-compose down -v
	@docker-compose -p $(COMPOSE_PROJECT_NAME)-integration down -v
	@docker-compose -p $(COMPOSE_PROJECT_NAME)-unit down -v
	@docker-compose rm -fsv
	@docker-compose -p $(COMPOSE_PROJECT_NAME)-integration rm -fsv
	@docker-compose -p $(COMPOSE_PROJECT_NAME)-unit rm -fsv

## Runs command `bash` commands in docker container.
bash:
	@docker exec -it $(PROJECT_NAME)-local bash

## Builds docker image
docker-build:
	@docker build $(IMAGE_TARGET) --build-arg version=$(GIT_STAMP) -t $(IMAGE) .
	@docker build --target=test --build-arg version=$(GIT_STAMP) -t $(IMAGE_TEST) .

## Runs integration tests | Tests
test-integration: $(REBUILD_IMAGES_FOR_TESTS)
	@docker rm -f $(PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) || true
	@docker-compose -p $(COMPOSE_PROJECT_NAME)-integration \
 	run --name $(PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) \
    $(PROJECT_NAME)-test-integration pytest -v -q --cov-report= --cov=prozorro_sale test/integration/
	@docker cp $(PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID):/$(PROJECT_NAME)/.coverage .coverage.integration

## Runs unit tests
test-unit: $(REBUILD_IMAGES_FOR_TESTS)
	@docker rm -f $(PROJECT_NAME)-unit-$(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) || true
	@docker-compose -p $(COMPOSE_PROJECT_NAME)-unit \
	run --name $(PROJECT_NAME)-unit-$(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) \
	$(PROJECT_NAME)-test-unit pytest -v -q --cov-report= --cov=prozorro_sale test/unit/
	@docker cp $(PROJECT_NAME)-unit-$(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID):/$(PROJECT_NAME)/.coverage .coverage.unit

# Linters & tests | Linters

## Formats code with `flake8`.
lint: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-test-unit bash -c "pip install flake8 && flake8 /$(PROJECT_NAME)/prozorro_sale"

## Safety checks your installed dependencies for known security vulnerabilities.
safety: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-test-unit bash -c "pip install safety && safety check --full-report"

## Bandit is a tool designed to find common security issues in Python code.
bandit: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-test-unit bash -c "pip install bandit && bandit -r /$(PROJECT_NAME)/prozorro_sale"

## Checks types with `mypy`.
mypy: docker-build
	@docker-compose run --rm $(PROJECT_NAME)-test-unit bash -c "pip install mypy && mypy --config-file=/.mypy.ini /$(PROJECT_NAME)/prozorro_sale"
{%- endif %}

## Create tag | Release
version:
	$(eval GIT_TAG ?= $(shell git describe --abbrev=0))
	$(eval VERSION ?= $(shell read -p "Version: " VERSION; echo $$VERSION))
	echo "Tagged release $(VERSION)\n" > Changelog-$(VERSION).txt
	git log --oneline --no-decorate --no-merges $(GIT_TAG)..HEAD >> Changelog-$(VERSION).txt
	git tag -a -e -F Changelog-$(VERSION).txt $(VERSION)


{%- if cookiecutter.use_helm == 'y' %}
## Build helm
helm-build: helm-dependency-update
	@helm3 package helm/$(PROJECT_NAME) --app-version=$(GIT_STAMP) --version=$(GIT_STAMP)$(HELM_STAMP)

## Dependency update helm
helm-dependency-update:
	@helm3 dependency update helm/$(PROJECT_NAME)

## Check helm
helm-lint: helm-dependency-update
	@helm3 lint helm/$(PROJECT_NAME)

## Check helm-kubeval
validate-helm-charts-kubeval: helm-dependency-update
	@helm3 kubeval --exit-on-error --strict --name-template=prozorro-dev-test --namespace=prozorro-dev-test helm/$(PROJECT_NAME)

## Publish helm
push-helm-package:
	@curl \
		--user $(CHART_MUSEUM_USER):$(CHART_MUSEUM_PASS) \
		--data-binary "@$(PROJECT_NAME)-$(GIT_STAMP)$(HELM_STAMP).tgz" \
		$(CHART_MUSEUM_URL)

{%- endif %}
{%- if cookiecutter.use_setup_py == 'y' %}
## Build python package
build-wheel:
	@python3 setup.py $(EGG_INFO) sdist bdist_wheel

## Publish python package
publish-wheel:
	twine upload --skip-existing dist/*

{%- endif %}
## Publish coverage report
publish-coverage:
	@docker rm -f $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) || true
	@docker run -d --name $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) $(IMAGE_TEST) sleep infinity
	@docker cp .coverage.unit $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID):/tmp/
	@docker cp .coverage.integration $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID):/tmp/
	@docker exec $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID) bash -c "cd /tmp && coverage combine && coverage report && coverage html -d cover-html"
	@docker cp $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID):/tmp/cover-html cover-html
	@docker rm -f $(CI_COMMIT_SHORT_SHA)$(CI_PIPELINE_ID)


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