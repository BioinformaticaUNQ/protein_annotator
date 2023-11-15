.PHONY: clean
clean: clean-build clean-pyc clean-test clean-venv
	rm -fr .mypy_cache/

.PHONY: clean-build
clean-build:
	: # Remove build artifacts
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '${SERVICE}-*.tgz' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc:
	: # Remove Python bytecode
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	: # Remove test artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache/

.PHONY: clean-venv
clean-venv:
	: # Remove virtual environment
	rm -fr .venv

.PHONY: venv
venv: clean
	: # Create venv
	python3 -m venv .venv

.PHONY: install
install: venv
	: # Activate venv and install protein_annotator for local development
	. .venv/bin/activate && pip install -e ".[dev,docs]"

.PHONY: test
test:
	: # Run pytest
	. .venv/bin/activate && pytest

.PHONY: coverage
coverage:
	: # Generate coverage report
	. .venv/bin/activate && coverage run

.PHONY: coverage-report
coverage-report:
	: # Generate HTML coverage report
	. .venv/bin/activate && coverage html
