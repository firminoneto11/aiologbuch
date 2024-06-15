cov := coverage run -m pytest
cov_port := 5500
url := http://localhost:$(cov_port)

env:
	rm -rf venv/
	python3.12 -m venv venv

deps:
	pip install --upgrade pip setuptools
	poetry install --no-root --all-extras

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -c "import webbrowser; webbrowser.open_new_tab('$(url)')"
	python -m http.server -d .coverage/html-report $(cov_port)
