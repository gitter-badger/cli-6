# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <jacoby@sparkl.com> Jacoby Thwaites
VERSION := $(shell git describe --tags --long --abbrev=1)
PY_VERSION := $(shell git describe --tags --abbrev=0)
.PHONY: deps
deps:
ifeq  '$(shell which pip)'  ''
	@echo "Missing pip, required for compile target"
	@echo "Consider '[apt-get|brew] install python-pip'"
endif
ifeq  '$(shell which pandoc)'  ''
	@echo "Missing pandoc, required for 'make rel' target"
	@echo "Consider '[apt-get|brew] install pandoc'"
endif
	@pip install --user -q pep8
	@pip install --user -q pylint
	@pip install --user -q pytest
	@pip install --user -q psutil
	@pip install --user -q argparse
	@pip install --user -q requests

# Note the -v displayed version is in the form v0.0.0-n-hash
.PHONY: compile
compile:
	@python -m pep8 sparkl_cli
	@python -m pylint --ignore=test sparkl_cli
	@python -m compileall sparkl_cli
	@echo ${VERSION} > sparkl_cli/version.txt

.PHONY: clean
clean:
	@find . -name "*.pyc" -exec rm {} \;

.PHONY: doc
doc:
	@echo No docs.

.PHONY: test
test:
	@python -m pytest

# Note the Python version is in form 0.0.0 only, where we rely
# on setuptools to normalise and remove the leading 'v'.
.PHONY: rel
rel: clean compile
ifeq  '$(shell which pandoc)'  ''
	$(error "Missing pandoc. Consider '[apt-get|brew] install pandoc'")
endif
	@sed s/{{version}}/\"${PY_VERSION}\"/ setup.py.src > setup.py
	@pandoc -o README.txt README.md
	@python setup.py sdist

.PHONY: clean_rel
clean_rel:
	@rm -f setup.py README.txt MANIFEST
	@rm -rf dist
