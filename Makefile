# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <jacoby@sparkl.com> Jacoby Thwaites
VERSION := $(shell git describe --tags --long --abbrev=1)
PY_VERSION := $(shell git describe --tags --abbrev=0)
.PHONY: deps
deps:
	@echo "If deps don't install, try doing 'sudo -H make deps'"
	@pip install pandoc
	@pip install pep8
	@pip install pylint
	@pip install pytest
	@pip install psutil
	@pip install argparse
	@pip install requests

# Note the -v displayed version is in the form v0.0.0-n-hash
.PHONY: compile
compile:
	@pep8 sparkl_cli
	@pylint --ignore=test sparkl_cli
	@python -m compileall sparkl_cli
	@echo ${VERSION} > sparkl_cli/version.txt

.PHONY: clean
clean:
	@find . -name "*.pyc" | xargs rm

.PHONY: doc
doc:
	@echo No docs.

.PHONY: test
test:
	@pytest

# Note the Python version is in form 0.0.0 only, where we rely
# on setuptools to normalise and remove the leading 'v'.
.PHONY: rel
rel: clean compile
	@sed s/{{version}}/\"${PY_VERSION}\"/ setup.py.src > setup.py
	@pandoc -o README.txt README.md
	@python setup.py sdist

.PHONY: clean_rel
clean_rel:
	@rm -f setup.py README.txt MANIFEST
	@rm -rf dist
