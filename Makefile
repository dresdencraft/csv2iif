.PHONY: install install-dev install-pipx test lint format run clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

install-pipx:
	pipx install .

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

run:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Usage: make run INPUT=<csv> OUTPUT=<iif>"; \
		exit 1; \
	fi
	python -m csv2iif $(INPUT) $(OUTPUT)

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .coverage htmlcov/ __pycache__/ */__pycache__/ */*/__pycache__/
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
