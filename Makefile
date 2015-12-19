MANAGE=bin/django
LOCALE=ru_RU.UTF-8

# Targets
.PHONY: run dbshell shell migrate

default: run

run:
	$(MANAGE) runserver

dbshell:
	$(MANAGE) dbshell

shell:
	$(MANAGE) shell

migrate:
	$(MANAGE) migrate
