.DEFAULT_GOAL := help
.PHONY := help view-docs test

SHELL=/bin/bash

pipenv_python ?= python3
pipenv = "`pipenv --venv`"
pipenv_bin = "$(pipenv)/bin"


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Installs project dependencies into pipenv
	@pipenv --venv || (pipenv --python $(pipenv_python); pipenv install -e .[all])

documentation: install  ## Builds the currently available documentation.
	@cp README.rst docs/source/introduction.rst
	@cp CHANGELOG.rst docs/source/changelog.rst
	@pipenv run sphinx-build -b html docs/source docs/

view-docs: port=8000
view-docs: documentation  ## Launches a Python HTTP server to view docs
	@$(pipenv_bin)/python -m http.server --bind 0.0.0.0 --dir docs $(port)

test: install  ## Runs project unit tests
	@$(pipenv_bin)/python -m unittest enummodel.tests

# upload-dist: test  ## Builds and uploads distribution
upload-dist: install  ## Builds and uploads distribution
	curl -XGET https://packages.wdt.pdx.edu/publish.sh | VENV=$(pipenv) bash -
	rm dist/*.whl
