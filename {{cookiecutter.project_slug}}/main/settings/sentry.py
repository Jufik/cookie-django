import sentry_sdk

from main.jsonenv import env
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env.get('sentry_dsn', ''),
    integrations=[DjangoIntegration()]
)
