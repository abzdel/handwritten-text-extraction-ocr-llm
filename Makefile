# Makefile for the vet-data-text-extraction project

# Install dependencies
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# Format Python code
format:
	black *.py
	black tests/*.py
	black setup/*.ipynb

# Lint Python code
lint:
	pylint --disable=R,C tests/*.py

# Run tests
test:
	pytest tests/test-invoke.py

# Target to run all tasks
all: install test format
