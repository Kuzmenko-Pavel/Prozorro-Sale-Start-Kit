
bandit:
	@bandit -r ./prozorro_sale_start_kit -x prozorro_sale_start_kit/template -s B101

checkrst:
	@python -m pep517.build . && python -m twine check dist/*

pyroma:
	@echo 'import setuptools; setuptools.setup()' > setup.py
	@pyroma -d .
	@rm setup.py

flake: checkrst bandit pyroma
	@flake8 prozorro_sale_start_kit

test:
	@rm -rf project-new/
	@pip install .
	@PssK --test Project-New
	@doc8 project-new/docs/
	@cd project-new/ && $(MAKE) lint test-integration test-unit

ci: flake test

clean:
	@rm -rf .eggs
	@rm -rf build
	@rm -rf dist
	@rm -rf prozorro_sale_start_kit.egg-info
	@rm -rf project-new
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

.PHONY: all flake test vtest cov clean doc ci

## Create tag
version:
	$(eval GIT_TAG ?= $(shell git describe --abbrev=0))
	$(eval VERSION ?= $(shell read -p "Version: " VERSION; echo $$VERSION))
	echo "Tagged release $(VERSION)\n" > Changelog-$(VERSION).txt
	git log --oneline --no-decorate --no-merges $(GIT_TAG)..HEAD >> Changelog-$(VERSION).txt
	git tag -a -e -F Changelog-$(VERSION).txt $(VERSION)