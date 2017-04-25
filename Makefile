# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <jacoby@sparkl.com> Jacoby Thwaites
.PHONY: deps
deps:
	@echo No deps.

.PHONY: compile
compile:
	@pep8 sparkl_cli
	@pylint --ignore=test sparkl_cli
	@python -m compileall sparkl_cli

.PHONY: clean
clean:
	@find . -name "*.pyc" | xargs rm

.PHONY: doc
doc:
	@echo No docs.

.PHONY: test
test:
	@python -m unittest discover

.PHONY: rel
rel: clean compile
	@sed s/{{version}}/\"`git describe --always`\"/ setup.py.src > setup.py
	@python setup.py sdist

.PHONY: clean_rel
clean_rel:
	@rm -f setup.py
	@rm -rf dist
