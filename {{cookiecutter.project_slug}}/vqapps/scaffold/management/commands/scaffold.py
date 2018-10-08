import os
import autopep8

from django.core.management.base import BaseCommand
from django.db.models import fields
from django.db.models.fields import related
from django.template import (Context, Template, loader)
from django.apps import apps

from vqapps.scaffold.factory_helpers import build_dependencies
from vqapps.scaffold.git_helper import GitClient


class Command(BaseCommand):
    help = """Generate factory-boy factories for the given app"""

    def add_arguments(self, parser):
        parser.add_argument('app', type=str)

    def handle(self, *args, **options):
        # git = GitClient()
        # git.handle_first_branch()
        # app.models gives "through" generated models
        app = apps.get_app_config(options['app'])
        models = list(app.get_models(include_auto_created=False))

        app_label = app.label
        context = {
            'app': app,
            'models': models,
            'app_label': app_label,
            'dependencies': build_dependencies(app.label, models)
        }

        scaffolds_path = os.path.join(app.path)
        if not os.path.exists(scaffolds_path):
            os.makedirs(scaffolds_path)

        tests_path = os.path.join(scaffolds_path, 'tests')
        if not os.path.exists(tests_path):
            os.makedirs(tests_path)
        open(os.path.join(tests_path, f'__init__.py'), 'w')

        for s in ['factory', 'serializers', 'api_views', 'rest_filters', 'resources']:
            code = loader.render_to_string(f'scaffold/{s}.html', context)
            with open(os.path.join(scaffolds_path, f'{s}.py'), 'w') as f:
                f.write(autopep8.fix_code(code))

        for s in ['test_models']:
            code = loader.render_to_string(f'scaffold/tests/{s}.html', context)
            with open(os.path.join(tests_path, f'{s}.py'), 'w') as f:
                f.write(autopep8.fix_code(code))

        for m in models:
            context['models'] = [m]
            code = loader.render_to_string(f'scaffold/tests/test_api.html', context)
            with open(os.path.join(tests_path, f'tests_{m.__name__.lower()}_api.py'), 'w') as f:
                f.write(autopep8.fix_code(code))
        # git.handle_second_branch()
