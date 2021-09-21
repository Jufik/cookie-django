from django.contrib.auth import login as django_login, logout as django_logout
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


from rest_framework import status, decorators, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.viewsets import GenericViewSet
from rest_auth.app_settings import create_token
from authentification.serializers import (
    LoginSerializer,
    TokenSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
)
from users.serializers import UserSerializer

from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode

from api.decorators import sensitive_post_parameters


class AuthViewset(GenericViewSet):
    class Meta:
        model = TokenModel

    @method_decorator(
        sensitive_post_parameters(
            "password", "old_password", "new_password1", "new_password2"
        )
    )
    @decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=LoginSerializer,
        url_name="login",
        url_path="login",
    )
    def login(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        self.serializer.is_valid(raise_exception=True)
        self.user = self.serializer.validated_data["user"]
        self.token = create_token(TokenModel, self.user, self.serializer)

        return Response(
            TokenSerializer(instance=self.token, context={"request": request},).data
        )

    @decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=serializers.Serializer,
        url_name="logout",
        url_path="logout",
    )
    def logout(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )

    @decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=PasswordResetSerializer,
        url_name="reset-password",
        url_path="reset-password",
    )
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )

    @decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=PasswordResetConfirmSerializer,
        url_name="reset-password-confirmation",
        url_path="reset-password-confirmation",
    )
    @method_decorator(
        sensitive_post_parameters(
            "password", "old_password", "new_password1", "new_password2"
        )
    )
    def reset_password_confirmation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )

    @decorators.action(
        detail=False,
        methods=["POST"],
        serializer_class=PasswordChangeSerializer,
        permission_classes=(IsAuthenticated,),
        url_name="change-password",
        url_path="change-password",
    )
    @method_decorator(
        sensitive_post_parameters(
            "password", "old_password", "new_password1", "new_password2"
        )
    )
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )

    @decorators.action(
        detail=False,
        methods=["GET"],
        serializer_class=UserSerializer,
        url_name="me",
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        # Return the success message with OK HTTP status
        return Response(serializer.data, status=status.HTTP_200_OK,)

