from django.core.management.templates import TemplateCommand
from django.conf import settings
import os

class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop('name')
        target = options.pop('directory')
        options['template'] = options.get('template') or './utils/app_template'
        with open(os.path.join(settings.BASE_DIR,"conftest.py"),"a") as conftest:
            conftest.write(f"from {app_name}.tests.conftest import * \r\n")
        super().handle('app', app_name, target, **options)
