import pytest
from django.core.exceptions import ImproperlyConfigured
from rest_framework import (
    mixins,
    views,
    viewsets,
    response,
    decorators,
    permissions,
    filters,
    generics,
    routers,
)

from api.viewsets import GenericViewSet
from api.models import TestModel

router = routers.DefaultRouter()


def test_api_view_without_meta_raises_an_error():
    with pytest.raises(ImproperlyConfigured) as e:

        class MockEndpoint(GenericViewSet):
            pass

    assert str(e.value) == "Meta should be defined on MockEndpoint"


def test_api_view_without_model_in_meta_raises_an_error():
    with pytest.raises(ImproperlyConfigured) as e:

        class MockEndpoint(GenericViewSet):
            class Meta:
                pass

    assert str(e.value) == "Meta in MockEndpoint should contain at least a model"


def test_api_view_without_model_in_meta_raises_an_error():
    with pytest.raises(ImproperlyConfigured) as e:

        class MockEndpoint(GenericViewSet):
            class Meta:
                model = None

    assert str(e.value) == "model:None in MockEndpoint Meta should inherirt from Model"


def test_api_view_with_model_returns_endpoint():
    class MockEndpoint(GenericViewSet):
        class Meta:
            model = TestModel

    assert hasattr(MockEndpoint, "queryset")
    assert hasattr(MockEndpoint, "serializer_class")
    assert hasattr(MockEndpoint, "search_fields")
    assert hasattr(MockEndpoint, "api")

    assert MockEndpoint.serializer_class == TestModel.Api.get_serializer("default")


def test_api_view_with_model_and_key_return_correct_serializer_class():
    class MockEndpoint(GenericViewSet):
        class Meta:
            model = TestModel
            key = "light"

    assert hasattr(MockEndpoint, "queryset")
    assert hasattr(MockEndpoint, "serializer_class")
    assert hasattr(MockEndpoint, "search_fields")
    assert hasattr(MockEndpoint, "api")

    assert MockEndpoint.serializer_class == TestModel.Api.get_serializer("light")


def test_viewsets_registers_to_api():
    class MockEndpoint(GenericViewSet):
        class Meta:
            model = TestModel
            key = "light"

    assert TestModel.Api.viewset == MockEndpoint

