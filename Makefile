install:
	pip install -e .

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*

tests:
	python -m pytest -v tests/
.PHONY: tests

regressions:
	python -m pytest -v tests/  --force-regen
.PHONY: tests