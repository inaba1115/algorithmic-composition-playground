.PHONY: all lint

all: lint

lint:
	poetry run black .
	poetry run isort . --profile black
	poetry run flake8 .
	poetry run mypy .
