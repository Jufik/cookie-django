from django.apps import AppConfig
from django.utils.translation import gettext as _
from api.options import BaseApi


class AuthConfig(AppConfig):
    name = "authentification"

    def ready(self):
        from rest_auth.models import TokenModel

        class Api(BaseApi):
            resource_name="auth"

        Api.contribute_to_class(TokenModel, "Api")
