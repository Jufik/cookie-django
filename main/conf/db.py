import os

DEBUG = os.getenv('PROD') is None

if DEBUG:
    import getpass
    USER = getpass.getuser()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('db_name'),
            'USER': USER,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('db_name'),
            'USER': os.environ.get('db_user'),
            'PASSWORD': os.environ.get('db_password'),
            'HOST': os.environ.get('db_host'),
            'PORT': '5432',
        }
    }
