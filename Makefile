
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
	@PssK --test project-new
	@doc8 project-new/docs/
	@cd project-new/ && $(MAKE) lint

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
