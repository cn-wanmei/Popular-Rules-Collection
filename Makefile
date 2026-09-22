.PHONY: all preflight collect build validate test

PYTHON ?= python
ENGINE := $(PYTHON) -m src.engine.cli
COLLECT := $(PYTHON) -m src.engine.collection

all:
	$(ENGINE) all

preflight:
	$(ENGINE) naming_gate

collect:
	$(COLLECT) --data data

build:
	$(ENGINE) adapters

validate:
	$(PYTHON) -m pytest tests/engine/ -v

test:
	$(PYTHON) -m pytest tests/engine/ -v
