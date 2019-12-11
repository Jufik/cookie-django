#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Specific to speed up tests
    from django.conf import settings
    if 'test' in sys.argv:
        import logging
        logging.disable(logging.CRITICAL)
        settings.DEBUG = False
        settings.TEMPLATE_DEBUG = False
        settings.DEFAULT_FILE_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
        settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
        settings.PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ]
    # end of specific
    execute_from_command_line(sys.argv)
