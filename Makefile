.PHONY: all preflight collect build validate test legacy-asset-audit

PYTHON ?= python
ENGINE := $(PYTHON) -m src.engine.cli
COLLECT := $(PYTHON) -m src.engine.collection
LEGACY_ASSET_EXTRACTOR := $(PYTHON) -m src.engine.ingest.legacy_asset_cli

all:
	$(ENGINE) all

preflight:
	$(ENGINE) naming_gate

collect:
	$(COLLECT) --data data

build:
	$(ENGINE) adapters

legacy-asset-audit:
	$(LEGACY_ASSET_EXTRACTOR) --rule-root rule --manifest data/legacy_asset_ir.yaml

validate:
	$(PYTHON) -m pytest tests/engine/ -v

test:
	$(PYTHON) -m pytest tests/engine/ -v
