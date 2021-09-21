import pytest
from api.schema.fields import FieldSchema, SerializerSchema
from api.models import TestModel, OtherTestModel
from api.schema.serializers import DumbSerializer, OtherTestModelSerializer
from rest_framework import serializers
from api.fields import RelatedFieldAlternative


@pytest.mark.xfail
def test_model_related_nested_serializer_with_many(model_serializer_factory):
    serializer = model_serializer_factory(
        "char_field",
        attrs={
            "dumb_nested_serializer": RelatedFieldAlternative(
                queryset=OtherTestModel.objects.all(),
                serializer=OtherTestModelSerializer,
            )
        },
    )
    # queryset=Group.objects.all(), serializer=GroupSerializer
    schema = SerializerSchema(serializer)

    assert "dumb_nested_serializer" in schema
    field = schema.get("dumb_nested_serializer")
    assert field.get("type") == "nested_many_related", field

    assert "resource" in field
    assert field.get("resource") == "other-test-models"
    assert "schema" in field

    nested_serializer = field.get("schema")
    assert "id" in nested_serializer
    nested_field = nested_serializer.get("id")
    assert nested_field.get("type") == "integer"


def test_model_related_nested_serializer_without_many(model_serializer_factory):
    serializer = model_serializer_factory(
        "char_field",
        attrs={
            "dumb_nested_serializer": OtherTestModelSerializer(source="foreign_key")
        },
    )

    schema = SerializerSchema(serializer)

    assert "dumb_nested_serializer" in schema
    field = schema.get("dumb_nested_serializer")
    assert field.get("type") == "nested_primary_key_related"

    assert "resource" in field
    assert field.get("resource") == "other-test-models"
    assert "schema" in field

    nested_serializer = field.get("schema")
    assert "id" in nested_serializer
    nested_field = nested_serializer.get("id")
    assert nested_field.get("type") == "integer"


@pytest.mark.xfail
def test_nested_serializer_with_many_without_source():
    raise NotImplementedError()


@pytest.mark.xfail
def test_nested_serializer_with_many_with_source():
    raise NotImplementedError()
