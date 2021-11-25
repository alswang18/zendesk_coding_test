.PHONY: format
format:
	poetry run black .
	poetry run isort . --profile black
	poetry run flake8 .  --ignore=W291 
.PHONY: pre-commit
pre-commit:
	poetry run black .
	poetry run isort . --profile black
	poetry run flake8 . --ignore=W291
	poetry run bandit .
	poetry run safety check