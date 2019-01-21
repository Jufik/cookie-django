from main.jsonenv import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # GeoDjango
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.get('db_name', ''),
        'USER': env.get('db_user', ''),
        'HOST': env.get('db_host', ''),
        'PASSWORD': env.get('db_password', ''),
        'PORT': '5432',
    }
}
