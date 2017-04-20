# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <jacoby@sparkl.com> Jacoby Thwaites
.PHONY: deps
deps:
	@echo No deps.

.PHONY: compile
compile:
	@python -m compileall sparkl

.PHONY: clean
clean:
	@rm sparkl/*.pyc

.PHONY: doc
doc:
	@echo No docs.

.PHONY: test
test:
	@echo No tests.

.PHONY: rel
rel: compile
