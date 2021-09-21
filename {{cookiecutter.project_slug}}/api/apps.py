from django.apps import AppConfig
from django.utils.translation import gettext as _
import importlib


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        from .options import registry

        for resource in registry.values():
            model = resource.model
            app_module = model.__module__.split(".")[:-1]
            importlib.import_module(".".join([*app_module, "serializers"]))
