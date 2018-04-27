from django.urls import path, include

from rest_framework import routers
from rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView
)

from emailauth.api_views import UserViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name="users")

rest_auth_urlpatters = [
    # URLs that do not require a session or valid token
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('login/', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
]

urlpatterns = [
    path('v1/', include([
        path('auth/', include(rest_auth_urlpatters)),

    ]))
]
