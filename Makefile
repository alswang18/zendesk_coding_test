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

.PHONY: test
test:
	poetry run pytest -p no:warnings --cov=.

.PHONY: run
run:
	poetry run python manage.py runserver 0.0.0.0:8000

.PHONY: demo-script
demo-script:
	chmod +x demo.sh
	./demo.sh