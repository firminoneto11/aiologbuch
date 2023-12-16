cov := coverage run -m pytest

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -m http.server -d .coverage/html-report 5500

build:
	python3 setup.py bdist_wheel sdist
