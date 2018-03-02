import os
import getpass

DEBUG = os.getenv('PROD') is None
USER = getpass.getuser()

_DATABASES = {
    'local': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('db_name'),
            'USER': USER,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    'remote': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('db_name'),
            'USER': os.environ.get('db_user'),
            'PASSWORD': os.environ.get('db_password'),
            'HOST': os.environ.get('db_host'),
            'PORT': '5432',
        }
    }
}


if DEBUG:
    DATABASES = _DATABASES['local']
else:
    DATABASES = _DATABASES['remote']
