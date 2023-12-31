cov := coverage run -m pytest

env:
	rm -rf venv/
	python3.12 -m venv venv

deps:
	poetry install --no-root

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -m http.server -d .coverage/html-report 5500

build:
	python3 setup.py bdist_wheel sdist
