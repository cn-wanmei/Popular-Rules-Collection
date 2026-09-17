.PHONY: all preflight collect build validate test legacy-asset-audit legacy-asset-reconcile

PYTHON ?= python
ENGINE := $(PYTHON) -m src.engine.cli
COLLECT := $(PYTHON) -m src.engine.collection
LEGACY_ASSET_EXTRACTOR := $(PYTHON) -m src.engine.ingest.legacy_asset_cli
LEGACY_ASSET_RECONCILER := $(PYTHON) -m src.engine.ingest.legacy_asset_reconciliation_cli

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

legacy-asset-reconcile:
	$(LEGACY_ASSET_RECONCILER) --rule-root rule --jsonl data/legacy_asset_ir.jsonl --report reports/v1/LEGACY_ASSET_RECONCILIATION.yaml --candidates reports/v1/V1_PROMOTION_CANDIDATES.yaml

validate:
	$(PYTHON) -m pytest tests/engine/ -v

test:
	$(PYTHON) -m pytest tests/engine/ -v
