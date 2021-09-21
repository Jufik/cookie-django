from api.schema.fields import FieldSchema, SerializerSchema
from api.models import TestModel, OtherTestModel
from api.schema.serializers import DumbSerializer, OtherTestModelSerializer
from rest_framework import serializers
from api.fields import RelatedFieldAlternative


def test_simple_nested_serializer(model_serializer_factory):
    serializer = model_serializer_factory(
        "char_field", attrs={"dumb_nested_serializer": DumbSerializer()}
    )

    schema = SerializerSchema(serializer)

    assert "dumb_nested_serializer" in schema
    field = schema.get("dumb_nested_serializer")
    assert field.get("type") == "object"
    assert "schema" in field

    nested_serializer = field.get("schema")
    assert "hello" in nested_serializer
    nested_field = nested_serializer.get("hello")
    assert nested_field.get("type") == "char"


def test_model_related_nested_serializer_with_many(model_serializer_factory):
    serializer = model_serializer_factory(
        "char_field",
        attrs={
            "dumb_nested_serializer": OtherTestModelSerializer(
                source="reverse_fks", many=True
            )
        },
    )

    schema = SerializerSchema(serializer)
    assert "dumb_nested_serializer" in schema
    field = schema.get("dumb_nested_serializer")
    assert field.get("type") == "nested_many_related"

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


def test_nested_serializer_with_many_without_source():
    pass


def test_nested_serializer_with_many_with_source():
    pass
