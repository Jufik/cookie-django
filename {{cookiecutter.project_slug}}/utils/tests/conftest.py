import pytest
from rest_framework.test import APIClient
from django.core.management import call_command
from django.shortcuts import reverse as url_reverse
from faker import Faker


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture()
def admin_client(db, admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.login(email=admin_user.email, password="password")
    return client


class DRFClient(APIClient):
    """
    Helper class used to test REST API
    """

    def __init__(self, *args, ressource=None, **kwargs):
        self.ressource = "api:%s" % ressource or ""
        super(DRFClient, self).__init__(*args, **kwargs)

    def authenticate(self, user):
        self.force_authenticate(user=user)

    @property
    def list_url(self):
        return url_reverse(self.ressource + "-list")

    def detail_url(self, *args):
        url = url_reverse(self.ressource + "-detail", args=(*args,))
        return url

    def custom_url(self, suffix, *args, **kwargs):
        url = url_reverse(f"{self.ressource}-{suffix}", args=(*args,))
        if kwargs:
            url += "?" + urlencode(kwargs)
        return url

    def create(self, data={}):
        return self.post(self.list_url, data)

    def list(self, data={}):
        return self.get(self.list_url, data)

    def retrieve(self, pk):
        return self.get(self.detail_url(pk))

    def update(self, pk, data):
        return self.patch(self.detail_url(pk), data)

    def destroy(self, pk):
        return self.delete(self.detail_url(pk))
