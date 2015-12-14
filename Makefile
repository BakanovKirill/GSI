MANAGE=bin/django
LOCALE=ru_RU.UTF-8

# Targets
.PHONY: run

default: run dbshell migrate

run:
	$(MANAGE) runserver

dbshell:
	$(MANAGE) dbshell

migrate:
	$(MANAGE) migrate
