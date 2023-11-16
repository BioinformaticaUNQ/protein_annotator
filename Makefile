.PHONY: clean
clean: clean-build clean-pyc clean-test
	rm -fr .mypy_cache/

.PHONY: clean-build
clean-build:
	: # Remove build artifacts
	rm -rf dist
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

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
venv: clean-venv
	: # Create venv
	python3 -m venv .venv

.PHONY: install
install: clean venv
	: # Activate venv and install protein_annotator for local development
	. .venv/bin/activate && pip install -e ".[dev,docs,release,test]"

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

.PHONY: build
build:
	: # Build artifacts
	. .venv/bin/activate && python -m build
