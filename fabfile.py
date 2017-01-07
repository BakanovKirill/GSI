# coding: utf-8
from fabric.api import *
import webbrowser
import os

from fab_local import GSI_APP_SERVER, REMOTE_CODE_DIR, ENV_PASS

env.password = ENV_PASS
env.hosts = [GSI_APP_SERVER]


def push_local_changes():
    local("git push origin master")


def pull_changes_on_remotes():
    with cd(REMOTE_CODE_DIR):
        run("git pull")


def clean_pyc():
	with cd(REMOTE_CODE_DIR):
		run('find . -name "*.pyc" -delete', shell=False)


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


def test_html():
    cur_dir = os.curdir
    full_path_cur_dir = os.path.abspath(os.curdir)
    path_to_cover_html = os.path.join(full_path_cur_dir, 'htmlcov')
    full_path_to_index = path_to_cover_html + '/index.html'

    local("coverage html")
    webbrowser.open(full_path_to_index)


def test_gsi():
    local("coverage run --source=gsi.tests bin/django test gsi.tests -v 2")
    test_html()


def test_cards():
    local("coverage run --source=cards.tests bin/django test cards.tests -v 2")
    test_html()


def create_docs():
    cur_dir = os.curdir
    full_path_cur_dir = os.path.abspath(os.curdir)
    path_to_docs_html = os.path.join(full_path_cur_dir, 'src/docs')

    with lcd(path_to_docs_html):
        local("make html")


def docs():
    cur_dir = os.curdir
    full_path_cur_dir = os.path.abspath(os.curdir)
    path_to_docs_html = os.path.join(full_path_cur_dir, 'src/docs/build/html')
    full_path_to_index = path_to_docs_html + '/index.html'
    create_docs()
    webbrowser.open(full_path_to_index)


def deploy():
    clean_pyc()
    push_local_changes()
    pull_changes_on_remotes()
    clean_pyc()
    restart()
