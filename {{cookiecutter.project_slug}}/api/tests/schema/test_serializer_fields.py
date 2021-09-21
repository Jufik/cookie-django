import pytest
from api.schema.fields import FieldSchema, SerializerSchema
from api.models import TestModel
from rest_framework import serializers


@pytest.mark.parametrize(
    "field_name,expected_type,extra_attrs,assertions",
    [
        ("binary_field", "model", [], []),
        ("boolean_field", "boolean", [], []),
        ("char_field", "char", [], []),
        ("char_field_with_choices", "choice", ["choices"], []),
        ("date_field", "date", [], []),
        ("date_time_field", "date_time", [], []),
        ("decimal_field", "decimal", [], []),
        ("duration_field", "duration", [], []),
        ("email_field", "email", [], []),
        ("float_field", "float", [], []),
        ("generic_ip_address_field", "ip_address", [], []),
        ("integer_field", "integer", [], []),
        # ("null_boolean_field", "null_boolean", [], []),
        ("positive_integer_field", "integer", [], []),
        ("positive_small_integer_field", "integer", [], []),
        ("slug_field", "slug", [], []),
        ("small_integer_field", "integer", [], []),
        ("text_field", "char", [], []),
        ("time_field", "time", [], []),
        ("url_field", "url", [], []),
        ("uuid_field", "uuid", [], []),
        ("file_field", "file", [], []),
        ("image_field", "image", [], []),
    ],
)
def test_basic_field_representation_on_model_serializer(
    field_name, expected_type, extra_attrs, assertions, model_serializer_factory
):

    schema = SerializerSchema(model_serializer_factory(field_name))
    assert field_name in schema
    field = schema.pop(field_name)

    for attr, value in assertions:
        assert field[attr] == value, (attr, value, field)

    for attr in [
        "read_only",
        "write_only",
        "required",
        "default",
        "label",
        "help_text",
        "allow_null",
        "allow_blank",
        "source",
    ]:
        field.pop(attr, None)

    assert field.pop("type") == expected_type

    for attr in ["validators", *extra_attrs]:
        assert attr in field
        field.pop(attr)

    assert len(field.keys()) == 0, field


@pytest.mark.parametrize(
    "field_name, extra_attrs,assertions",
    [
        ("foreign_key", [], [("filters", {"char_field__icontains": "hello"})]),
        ("many_to_many_field", [], [("filters", {"char_field__icontains": "world"})]),
        ("one_to_one_field", [], [("filters", {})]),
        ("reverse_many_with_through", [], []),
        ("reverse_fks", [], []),
        ("reverse_one", [], []),
    ],
)
def test_related_fields_on_model_serializer(
    field_name, extra_attrs, assertions, model_serializer_factory
):
    schema = SerializerSchema(model_serializer_factory(field_name))
    assert schema.model is not None
    assert field_name in schema
    field = schema.get(field_name)

    assert field.serializer_schema.model is not None
    assert field.has_through_model is not None
    assert field.related_model is not None
    assert field.reverse in [True, False]
    assert field.to_many is not None
    # assert field.related_model is not None
    assert "resource" in field
    assert field.pop("resource") == "other-test-models"

    for attr in [
        "read_only",
        "write_only",
        "required",
        "default",
        "label",
        "help_text",
        "allow_null",
        "allow_blank",
        "source",
    ]:
        field.pop(attr, None)

    for attr, value in assertions:
        assert attr in field, schema
        result = field.pop(attr)
        assert result == value, (attr, value, field)

    for attr in ["type", "validators", *extra_attrs]:
        assert attr in field, schema
        field.pop(attr)

    assert len(field.keys()) == 0, field


@pytest.mark.xfail
def test_nested_serializer_without_source():
    raise NotImplementedError()


@pytest.mark.xfail
def test_nested_serializer_with_source():
    raise NotImplementedError()


@pytest.mark.xfail
def test_nested_serializer_with_many_without_source():
    raise NotImplementedError()


@pytest.mark.xfail
def test_nested_serializer_with_many_with_source():
    raise NotImplementedError()
