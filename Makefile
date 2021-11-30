.PHONY: format
format:
	poetry run black .
	poetry run isort . --profile black
	poetry run flake8 .  --ignore=W291,W503

.PHONY: pre-commit
pre-commit:
	make format
	poetry run bandit .
	poetry run safety check

.PHONY: test
test:
	poetry run pytest -p no:warnings --cov=.

.PHONY: run
run:
	poetry run python manage.py runserver 0.0.0.0:8000

.PHONY: demo-script-run
demo-script-run:
	chmod +x demo.sh
	./demo.sh
	make run

.PHONY: demo-script-test
demo-script-test:
	chmod +x demo.sh
	./demo.sh
	make test
