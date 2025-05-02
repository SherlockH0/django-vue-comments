.PHONY: install 
install:
	poetry install

.PHONY: migrate
migrate: 
	poetry run python -m backend.manage migrate

.PHONY: migrations 
migrations: 
	poetry run python -m backend.manage makemigrations
	
.PHONY: runserver
runserver:
	poetry run python -m backend.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m backend.manage createsuperuser

.PHONY: shell
shell:
	poetry run python -m backend.manage shell

.PHONY: celery
celery:
	poetry run celery -A backend.project worker -l INFO

.PHONY: update
update: install migrate ;
