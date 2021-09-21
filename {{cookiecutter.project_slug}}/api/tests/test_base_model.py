import pytest
from api.models import TestModel, TestThrough, OtherTestModel
from api.options import ApiMeta, AlreadyRegisteredException, registry, BaseApi
from api.serializers import ModelSerializer


def test_model_as_Api(db,):
    assert hasattr(TestModel, "Api")
    assert hasattr(TestModel.Api, "serializer_store")
    assert isinstance(TestModel.Api, BaseApi)


def test_api_registers_serializer_with_get_serializer(db):

    assert TestModel.Api.serializer_store == {}
    TestModel.Api.get_serializer("default")
    assert "default" in TestModel.Api.serializer_store


def test_api_registers_serializer_outsde_api(db):

    TestModel.Api.get_serializer("default")
    assert "default" in TestModel.Api.serializer_store

    class OtherTestModelSerializer(ModelSerializer):
        class Meta:
            model = TestModel
            fields = ["char_field"]

    assert "other" in TestModel.Api.serializer_store
    assert hasattr(OtherTestModelSerializer.Meta, "key")
    assert OtherTestModelSerializer.Meta.key == "other"


def test_api_registering_serializer_with_clashing_name_raises_an_error(db):

    TestModel.Api.get_serializer("default")
    assert "default" in TestModel.Api.serializer_store

    with pytest.raises(AlreadyRegisteredException):

        class TestModelSerializer(ModelSerializer):
            class Meta:
                model = TestModel
                fields = ["char_field"]


def test_model_registered(db):
    assert "test-models" in registry, registry
