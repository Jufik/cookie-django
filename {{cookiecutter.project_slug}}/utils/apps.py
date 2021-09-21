import logging

from django.apps import AppConfig
from django.utils.translation import gettext as _


class UtilsConfig(AppConfig):
    name = "utils"
    # verbose_name = _("Utils")

    def ready(self):
        super().ready()
        from django.conf import settings
        from main.jsonenv import env_file

        logger = logging.getLogger("django")
        logger.info(f"DEBUG:{settings.DEBUG}")
        logger.info(f"LOADING CREDS FROM FILE {env_file}")
