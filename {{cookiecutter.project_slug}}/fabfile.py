import datetime
import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.utils import abort
from fabric.operations import prompt
from main.jsonenv import env as creds_env


env.user = 'ec2-user'
env.hosts = ['{{cookiecutter.host_ip}}']

def dump_db():
    if confirm("This will dump database %s (%s), Continue ?" % (creds_env.get('db_name', ''), creds_env.get('db_host', '')), default=False):
        local('PGPASSWORD=%s pg_dump --dbname=%s --host=%s --username=%s > dumps/db-remote-%s.sql' % (
            creds_env.get('db_password', ''),
            creds_env.get('db_name', ''),
            creds_env.get('db_host', ''),
            creds_env.get('db_user', ''),
            datetime.datetime.now().replace(microsecond=0).isoformat()
        ))

def create_local_db():
    local("createdb '%s'" % creds_env.get('db_name', ''))
    print('Local database %s successfully created' % creds_env.get('db_name', '') )

def drop_local_db():
    local("dropdb --if-exists '%s'" % creds_env.get('db_name', ''))

def import_dump():
    print('Select the dump you would like to import :')
    dumps = []
    for file_ in os.listdir("/dumps"):
        if file_.endswith(".sql"):
            dumps.append(os.path.join("/dumps", file_))
    for counter, db in enumerate(dumps):
        print("\t{counter}) {db}")
    selected_dump_index = prompt("Your choice: ", validate=int)
    try:
        selected_dump = dumps[selected_dump_index]
    except IndexError:
        abort('%s is not a valid choice')
    if confirm("This will replace local database %s with dump %s, Continue ?" % (
            creds_env.get('db_name', ''),
            selected_dump),
            default=False):
        drop_local_db()
        create_local_db()
        local("psql --dbname=%s < %s" % (creds_env.get('db_name', ''), selected_dump))

def deploy():
    with cd('/home/ec2-user/{{cookiecutter.project_slug}}'):
        run("git pull")
        run("source venv/bin/activate && PYTHON_INSTALL_LAYOUT="" pip install -r requirements.txt")
        run("source venv/bin/activate && ./manage.py collectstatic --noinput --ignore *.scss")
        run("venv/bin/uwsgi --reload {{cookiecutter.project_slug}}.pid")


def migrate():
    with cd('/home/ec2-user/{{cookiecutter.project_slug}}'):
        run("source venv/bin/activate && PROD=1 ./manage.py migrate")


def pull():
    with cd('/home/ec2-user/{{cookiecutter.project_slug}}'):
        run("git pull")


def reload():
    with cd('/home/ec2-user/{{cookiecutter.project_slug}}'):
        run("git pull")
        run("venv/bin/uwsgi --reload {{cookiecutter.project_slug}}.pid")

def nginx():
    with cd('/home/ec2-user/{{cookiecutter.project_slug}}'):
        run("sudo cp conf/{{cookiecutter.project_slug}}.conf /etc/nginx/conf.d/" % project_name)
        run("sudo service nginx restart")

def commit(message):
    local("git add --all")
    local("git commit -m \"%s\"" % message)
    local("git push")


def cdeploy(message):
    commit(message)
    deploy()


def start():
    with cd('/home/ec2-user'):
        run("git clone https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}.git")
    with cd('/home/ec2-user/{{cookiecutter.project_slug}}'):
        run("virtualenv venv -p python3")
        run("source venv/bin/activate && PYTHON_INSTALL_LAYOUT="" pip install -U pip")
        run("source venv/bin/activate && PYTHON_INSTALL_LAYOUT="" pip install uwsgi")
        run("source venv/bin/activate && PYTHON_INSTALL_LAYOUT="" pip install -r requirements.txt")
        run("source venv/bin/activate && ./manage.py collectstatic --noinput --ignore *.scss")
        run("venv/bin/uwsgi {{cookiecutter.project_slug}}.ini")
        run("sudo cp {{cookiecutter.project_slug}}.conf /etc/nginx/conf.d/")
        run("sudo service nginx restart")
