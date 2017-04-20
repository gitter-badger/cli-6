# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <jacoby@sparkl.com> Jacoby Thwaites
.PHONY: deps
deps:
	@echo No deps.

.PHONY: compile
compile:
	@pep8 sparkl_cli
	@pylint sparkl_cli
	@python -m compileall sparkl_cli

.PHONY: clean
clean:
	@rm sparkl_cli/*.pyc

.PHONY: doc
doc:
	@echo No docs.

.PHONY: test
test:
	@echo No tests.

.PHONY: rel
rel: compile
