import pytest
from django.urls import path, include, reverse
from django.test import override_settings
from rest_framework import routers
from rest_framework.test import APIClient, force_authenticate
from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from authentification.api_views import AuthViewset
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode


router = routers.DefaultRouter()

router.register("auth", AuthViewset, basename="auth")
urlpatterns = [
    path("", include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
def test_login_with_successful_cred(db, user):
    user.set_password("password")
    user.save()
    client = APIClient()
    response = client.post(
        reverse("auth-login"), data={"email": user.email, "password": "password"}
    )
    assert response.status_code == 200, response.content


@override_settings(ROOT_URLCONF=__name__)
def test_login_with_failing_creds(db, user):
    client = APIClient()
    response = client.post(
        reverse("auth-login"), data={"email": user.email, "password": "password"}
    )
    assert response.status_code == 400, response.content


@override_settings(ROOT_URLCONF=__name__)
def test_lougout_with_loged_in_user(db, user):
    token = TokenModel.objects.get_or_create(user=user)

    assert getattr(user, "auth_token", None) is not None
    client = APIClient()
    client.force_authenticate(user, token)
    response = client.post(
        reverse("auth-logout"), data={"email": user.email, "password": "password"}
    )
    user.refresh_from_db()
    assert response.status_code == 200, response.content
    assert getattr(user, "auth_token", None) is None


@override_settings(ROOT_URLCONF=__name__)
def test_lougout_with_anonymous_user(db, user):
    client = APIClient()
    response = client.post(
        reverse("auth-logout"), data={"email": user.email, "password": "password"}
    )
    assert response.status_code == 200, response.content


@pytest.mark.xfail  # Needs to overrid default serializer
@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_with_existing_custom(db, user):
    client = APIClient()
    response = client.post(reverse("auth-reset-password"), data={"email": user.email})
    assert response.status_code == 200, response.content


@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_with_inexisting_custom(db, user):
    client = APIClient()
    response = client.post(
        reverse("auth-reset-password"), data={"email": "hello@world.com"}
    )
    assert response.status_code == 200, response.content


@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_confirmation_success(db, user):
    client = APIClient()
    response = client.post(
        reverse("auth-reset-password-confirmation"),
        data={
            "new_password1": "helloWorld20202",
            "new_password2": "helloWorld20202",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    assert response.status_code == 200, response.content
    user.refresh_from_db()
    assert user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_confirmation_checks_password_value(db, user):
    client = APIClient()
    response = client.post(
        reverse("auth-reset-password-confirmation"),
        data={
            "new_password1": "azerty",
            "new_password2": "azerty",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    assert response.status_code == 400
    assert "new_password2" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_confirmation_fails_when_password_are_different(db, user):
    client = APIClient()
    response = client.post(
        reverse("auth-reset-password-confirmation"),
        data={
            "new_password1": "helloWorld20202",
            "new_password2": "helloWorld202021",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    assert response.status_code == 400
    assert "new_password2" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_confirmation_fails_when_token_do_not_match(
    db, user, user_factory
):
    client = APIClient()
    response = client.post(
        reverse("auth-reset-password-confirmation"),
        data={
            "new_password1": "helloWorld20202",
            "new_password2": "helloWorld20202",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user_factory()),
        },
    )
    assert response.status_code == 400
    assert "token" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
def test_reset_password_confirmation_fails_when_uid_do_not_match(
    db, user, user_factory
):
    client = APIClient()
    response = client.post(
        reverse("auth-reset-password-confirmation"),
        data={
            "new_password1": "helloWorld20202",
            "new_password2": "helloWorld20202",
            "uid": urlsafe_base64_encode(force_bytes(user.pk + 1)),
            "token": default_token_generator.make_token(user),
        },
    )
    assert response.status_code == 400
    assert "uid" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
def test_change_password_when_logged_out(db, user):
    user.save()
    client = APIClient()
    response = client.post(
        reverse("auth-change-password"),
        data={"email": user.email, "password": "password"},
    )
    assert response.status_code == 401, response.content


@override_settings(ROOT_URLCONF=__name__)
@override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
def test_change_password_when_both_old_and_new_passwords_are_valid(db, user):
    user.set_password("password")
    user.save()
    client = APIClient()
    client.force_authenticate(user)
    response = client.post(
        reverse("auth-change-password"),
        data={
            "old_password": "password",
            "new_password1": "helloWorld20202",
            "new_password2": "helloWorld20202",
        },
    )
    assert response.status_code == 200, response.content
    user.refresh_from_db()
    assert user.check_password("helloWorld20202")


@pytest.mark.xfail  # Works but depends on Confifuration initialization
@override_settings(ROOT_URLCONF=__name__)
@override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
def test_change_password_when_old_password_do_not_match(db, user):
    user.set_password("password")
    user.save()
    client = APIClient()
    client.force_authenticate(user)
    response = client.post(
        reverse("auth-change-password"),
        data={
            "old_password": "passsssworsd",
            "new_password1": "helloWorld20202",
            "new_password2": "helloWorld20202",
        },
    )
    assert response.status_code == 400, response.content
    assert "old_password" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
@override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
def test_change_password_when_new_password_do_not_match(db, user):
    user.set_password("password")
    user.save()
    client = APIClient()
    client.force_authenticate(user)
    response = client.post(
        reverse("auth-change-password"),
        data={
            "old_password": "password",
            "new_password1": "helloWorld202021",
            "new_password2": "helloWorld20202",
        },
    )
    assert response.status_code == 400, response.content
    assert "new_password2" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
@override_settings(OLD_PASSWORD_FIELD_ENABLED=False)
def test_change_password_when_new_passwords_are_valid_and_old_password_not_required(
    db, user
):
    user.set_password("password")
    user.save()
    client = APIClient()
    client.force_authenticate(user)
    response = client.post(
        reverse("auth-change-password"),
        data={"new_password1": "helloWorld20202", "new_password2": "helloWorld20202",},
    )
    assert response.status_code == 200, response.content
    user.refresh_from_db()
    assert user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
@override_settings(OLD_PASSWORD_FIELD_ENABLED=False)
def test_change_password_when_new_password_do_not_match_and_old_password_not_required(
    db, user
):
    user.set_password("password")
    user.save()
    client = APIClient()
    client.force_authenticate(user)
    response = client.post(
        reverse("auth-change-password"),
        data={"new_password1": "helloWorld202021", "new_password2": "helloWorld20202",},
    )
    assert response.status_code == 400, response.content
    assert "new_password2" in response.data
    user.refresh_from_db()
    assert not user.check_password("helloWorld20202")


@override_settings(ROOT_URLCONF=__name__)
def test_me_with_logged_in_user(db, user):
    token = TokenModel.objects.get_or_create(user=user)
    assert getattr(user, "auth_token", None) is not None
    client = APIClient()
    client.force_authenticate(user, token)
    response = client.get(reverse("auth-me"))
    assert response.status_code == 200, response.content
    assert response.data.get("id") == user.pk


@override_settings(ROOT_URLCONF=__name__)
def test_me_with_anonymous(db, user):
    client = APIClient()
    response = client.get(reverse("auth-me"))
    assert response.status_code == 401, response.content

