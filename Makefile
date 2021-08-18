install:
	pip install -e .

build:
	echo "TODO"

tests:
	python -m pytest -v tests/
.PHONY: tests

regressions:
	python -m pytest -v tests/  --force-regen
.PHONY: tests