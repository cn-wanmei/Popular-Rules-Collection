.PHONY: all preflight collect build validate test

PYTHON ?= python
ENGINE := $(PYTHON) -m src.engine.cli

all:
	$(ENGINE) all

preflight:
	$(ENGINE) naming_gate

collect:
	$(ENGINE) collect

build:
	$(ENGINE) adapters

validate:
	$(ENGINE) validate

test:
	$(PYTHON) -m pytest tests/engine/ -v --ignore=tests/engine/unit_legacy_v2_ref
