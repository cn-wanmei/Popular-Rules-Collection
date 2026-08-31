.PHONY: preflight collect normalize build validate pipeline

preflight:
	python scripts/pipeline.py preflight

collect:
	python scripts/pipeline.py collect

normalize:
	python scripts/pipeline.py normalize

build:
	python scripts/pipeline.py build

validate:
	python scripts/pipeline.py validate

pipeline:
	python scripts/pipeline.py all
