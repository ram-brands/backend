.PHONY: getpoetry
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

.PHONY: createvenv
createvenv:
	python3 -m venv .venv
	poetry run pip3 install --upgrade pip
	poetry run poetry install

.PHONY: localsettings
localsettings:
	cp ramws/core/local_settings.example.py ramws/core/local_settings.py

.PHONY: black
black:
	poetry run black ramws --check

.PHONY: black!
black!:
	poetry run black ramws

.PHONY: isort
isort:
	poetry run isort ramws --check

.PHONY: isort!
isort!:
	poetry run isort ramws

.PHONY: format!
format!: black! isort!

.PHONY: build
build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build

.PHONY: tests
tests:
	docker-compose run web python manage.py test

.PHONY: shell
shell:
	docker-compose run web python manage.py shell_plus --plain

.PHONY: migrate
migrate:
	docker-compose run web python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker-compose run web python manage.py makemigrations
