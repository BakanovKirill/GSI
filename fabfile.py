# coding: utf-8
from fabric.api import *

from fab_local import GSI_APP_SERVER, REMOTE_CODE_DIR, ENV_PASS

env.password = ENV_PASS
env.hosts = [GSI_APP_SERVER]


def push_local_changes():
    local("git push origin master")


def pull_changes_on_remotes():
    with cd(REMOTE_CODE_DIR):
        run("git pull")


def restart():
    with cd(REMOTE_CODE_DIR):
        sudo("service supervisor restart")


def restart_ngnix():
    with cd(REMOTE_CODE_DIR):
        sudo("service nginx restart")


def migrate():
    with cd(REMOTE_CODE_DIR):
        run("bin/django migrate")


def collectstatic():
    with cd(REMOTE_CODE_DIR):
        run("bin/django collectstatic")


def ngnix():
    restart_ngnix()
    restart()


def update():
    with cd(REMOTE_CODE_DIR):
        run("bin/buildout")


def fill_name_carditem():
    with cd(REMOTE_CODE_DIR):
        run("bin/django fill_name_for_carditem_card")


@hosts(GSI_APP_SERVER)
def update_dev_db():
    """
	Get fresh copy of database from prod to local.
	"""
    with cd("/tmp"), lcd("/tmp"):
        sudo("pg_dump gsi > /tmp/latest.sql", user="postgres")
        run("tar zcvf latest.sql.tgz latest.sql")
        get("/tmp/latest.sql.tgz", "latest.sql.tgz")
        sudo("rm /tmp/latest.sql.tgz /tmp/latest.sql")

        local("dropdb gsi")
        local("createdb gsi")
        local("tar zxvf latest.sql.tgz")
        local("psql gsi < latest.sql")
        local("rm latest.sql latest.sql.tgz")


def deploy():
    push_local_changes()
    pull_changes_on_remotes()
    restart()
