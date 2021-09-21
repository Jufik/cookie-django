from main.jsonenv import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # GeoDjango
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.get('db_name', ''),
        'USER': env.get('db_user', ''),
        'HOST': env.get('db_host', ''),
        'PASSWORD': env.get('db_password', ''),
        'PORT':  env.get('db_port', '5432'),
    }
}
