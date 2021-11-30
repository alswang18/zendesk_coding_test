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

.PHONY docker:
docker:
	docker-compose up --build -d

make docker-no-build:
docker-no-build:
	docker-compose up -d

.PHONY docker-test:
docker-test:
	make docker-no-build
	docker-compose exec app make test

.PHONY docker-pre-commit:
docker-pre-commit:
	make docker-no-build
	docker-compose exec app make pre-commit

.PHONY setup-local:
setup-local:
	pip install poetry==1.1.11
	poetry install