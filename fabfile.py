from __future__ import with_statement

import getpass
import os
from fabric.api import *
from main.conf.db import DATABASES

env.user = 'ec2-user'
env.hosts = ['']
env.key_filename = ['~/GIT/__keys/my_key.pem']

project_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

USER = getpass.getuser()


def importdb():
    print("Export DB")
    local('PGPASSWORD="%s" pg_dump --dbname=%s --host=%s --username=%s > dump.sql' % (
        DATABASES['default']['PASSWORD'],
        DATABASES['default']['NAME'],
        DATABASES['default']['HOST'],
        DATABASES['default']['USER'],))


def loaddb():
    print("Importing DB")
    local("sudo -u %s psql -c 'drop database if exists %s;'" % (USER, project_name))
    local("sudo -u %s psql -c 'create database %s;'" % (USER, project_name))
    local("psql --dbname=%s < ./dump.sql" % (project_name))


def create_local_db():
    print("Creating local DB")
    local("sudo -u %s psql -c 'create database %s;'" % (USER, project_name))


def syncdb():
    importdb()
    loaddb()


def stagging():
    with cd('/home/ec2-user/stagging_%s' % project_name):
        run("git pull")
        run("source venv/bin/activate && pip install -r requirements.txt")
        run("source venv/bin/activate && DOMAIN_PROD=STAGGING PROD=1 ./manage.py collectstatic --noinput --ignore *.scss")
        run("venv/bin/uwsgi --reload %s.pid" % project_name)


def deploy():
    with cd('/home/ec2-user/%s' % project_name):
        run("git pull")
        run("source venv/bin/activate && pip install -r requirements.txt")
        run("source venv/bin/activate && DOMAIN_PROD=PROD PROD=1 ./manage.py collectstatic --noinput --ignore *.scss")
        run("venv/bin/uwsgi --reload %s.pid" % project_name)


def migrate():
    with cd('/home/ec2-user/%s' % project_name):
        run("source venv/bin/activate && PROD=1 ./manage.py migrate")


def pull():
    with cd('/home/ec2-user/%s' % project_name):
        run("git pull")


def reload():
    with cd('/home/ec2-user/%s' % project_name):
        run("git pull")
        run("venv/bin/uwsgi --reload %s.pid" % project_name)


def nginx():
    with cd('/home/ec2-user/%s' % project_name):
        run("sudo cp %s.conf /etc/nginx/conf.d/" % project_name)
        run("sudo service nginx restart")


def commit(message):
    local("git add --all")
    local("git commit -m \"%s\"" % message)
    local("git push")


def cdeploy(message):
    commit(message)
    deploy()


def cstagging(message):
    commit(message)
    stagging()


def start():
    with cd('/home/ec2-user'):
        run("git clone https://gitlab.com/e-reflex/%s.git" % project_name)
    with cd('/home/ec2-user/%s' % project_name):
        run("virtualenv venv")
        run("source venv/bin/activate && pip install -U pip")
        run("source venv/bin/activate && pip install uwsgi")
        run("source venv/bin/activate && pip install -r requirements.txt")
        run("source venv/bin/activate && ./manage.py collectstatic --noinput --ignore *.scss")
        run("venv/bin/uwsgi %s.ini" % project_name)
        run("sudo cp %s.conf /etc/nginx/conf.d/" % project_name)
        run("sudo service nginx restart")
