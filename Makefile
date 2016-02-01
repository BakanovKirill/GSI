MANAGE=bin/django
LOCALE=ru_RU.UTF-8

# Targets
.PHONY: run dbshell shell mkmigr_gsi migrate migrate_gsi mkmigr_cards migrate_cards test_gsi test_cards deploy static restart

default: run

run:
	$(MANAGE) runserver

dbshell:
	$(MANAGE) dbshell

shell:
	$(MANAGE) shell

migrate:
	$(MANAGE) migrate

mkmigr_gsi:
	$(MANAGE) makemigrations gsi

migrate_gsi:
	$(MANAGE) migrate gsi

mkmigr_cards:
	$(MANAGE) makemigrations cards

migrate_cards:
	$(MANAGE) migrate cards

test_gsi:
	$(MANAGE) test gsi

test_cards:
	$(MANAGE) test cards

deploy:
	fab deploy

static:
	$(MANAGE) collectstatic
	fab collectstatic

restart:
    fab restart
