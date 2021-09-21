import pytest
from api.schema.fields import FieldSchema, SerializerSchema, FieldAlreadyTypeException
from api.models import TestModel
from rest_framework import serializers


def test_field_schema_raises_an_error_when_type_is_set_multiple_times(
    model_serializer_factory,
):

    schema = SerializerSchema(model_serializer_factory("char_field"))
    field = schema.get("char_field")
    with pytest.raises(FieldAlreadyTypeException):
        field.set_type("hello")
