build:
	rm -rf build/ conduits.egg-info/ dist/
	python setup.py sdist bdist_wheel
.PHONY: build

publish: build
	twine upload dist/*

tests:
	python -m pytest -v tests/
.PHONY: tests

regressions:
	python -m pytest -v tests/  --force-regen
.PHONY: tests