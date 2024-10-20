# Makefile for the vet-data-text-extraction project

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py
	black tests/*.py

lint:
	pylint --disable=R,C tests/*.py

test:
	pytest tests/

all: install test format
