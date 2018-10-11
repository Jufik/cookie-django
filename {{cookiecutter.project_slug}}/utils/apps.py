import logging

from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = 'utils'

    def ready(self):
        super().ready()
        from django.conf import settings
        from main.jsonenv import env_file
        logger = logging.getLogger('django')
        logger.info(f'DEBUG:{settings.DEBUG}')
        logger.info(f'LOADING CREDS FROM FILE {env_file}')

