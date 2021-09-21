from api.schema.mappings import SERIALIZER_FIELDS_MAP, VALIDATORS_MAP
from rest_framework.fields import empty, _UnvalidatedField
from rest_framework import serializers, fields
from rest_framework.utils import model_meta
from rest_framework.schemas.inspectors import ViewInspector
from collections import OrderedDict


class FieldAlreadyTypeException(Exception):
    pass


class FieldSchema(dict):
    def __init__(self, fieldname, field, serializer_schema):
        self.fieldname = fieldname
        self.field = field
        self.serializer_schema = serializer_schema

        self.field_mapping = SERIALIZER_FIELDS_MAP.get(self.field.__class__)

        self.init_model_field()
        self.build()

    def build(self):
        self.set_field_type()
        self.set_attrs()
        self.set_related()
        self.set_validators()

    def set_type(self, _type):
        if "type" in self:
            raise FieldAlreadyTypeException(
                f"Type {self['type']} already set in {self.fieldname}"
            )
        else:
            self["type"] = _type

    def set_field_type(self):
        if self.field_mapping:
            self.set_type(self.field_mapping.get("type"))
            return

        base_type = None
        child_serializer = None
        if isinstance(self.field, serializers.ListSerializer):
            child_serializer = self.field.child
            self["schema"] = SerializerSchema(child_serializer)
            base_type = "list"

        if isinstance(self.field, serializers.Serializer):
            child_serializer = self.field
            self["schema"] = SerializerSchema(self.field)
            base_type = "object"

        if isinstance(child_serializer, serializers.ModelSerializer):
            self.set_type(
                {
                    "list": "nested_many_related",
                    "object": "nested_primary_key_related",
                }.get(base_type)
            )
        else:
            self.set_type(base_type)

        if self.get("type", None) is None:
            raise Exception(f"Should get a type for {self.fieldname} with {self.field}")

    def set_attrs(self):
        attrs = [
            "read_only",
            "write_only",
            "required",
            "default",
            "label",
            "source",
            "help_text",
            "allow_null",
            "allow_blank",
            "style",
        ]

        for attr in attrs:
            value = getattr(self.field, attr, None)
            if value is not None and value != empty and not callable(value):
                if type(value) == dict:
                    self.update(value)
                else:
                    self[attr] = value
        self.pop("base_template","")
    def set_validators(self):
        self["validators"] = []
        for validator in self.field.validators:
            cls = validator.__class__
            _map = VALIDATORS_MAP.get(cls, None)
            if _map:
                self["validators"].append(
                    {
                        "name": _map.get("name"),
                        **{
                            key: getattr(validator, value)
                            for key, value in _map.get("values").items()
                        },
                    }
                )

    def set_related(self):
        if self.related_model:
            self["resource"] = "-".join(
                self.related_model._meta.verbose_name_plural.lower().split()
            )
        elif (
            (value := getattr(self.field, "choices", None)) is not None
            and value != empty
            and not callable(value)
        ):
            self["choices"] = value

        if self.model_field and hasattr(self.model_field, "get_limit_choices_to"):
            self["filters"] = self.model_field.get_limit_choices_to()

    @property
    def is_related(self):
        return self.related_model is not None

    def init_model_field(self):
        self.model = self.serializer_schema.model
        self.has_through_model = None
        self.model_field = None
        self.related_model = None
        self.reverse = None
        self.to_field = None
        self.to_many = None
        if self.model is None:
            return

        else:
            model_info = model_meta.get_field_info(self.model)
            if (relation := model_info.relations.get(self.field.source)) is not None:
                self.has_through_model = relation.has_through_model
                self.model_field = relation.model_field
                self.related_model = relation.related_model
                self.reverse = relation.reverse
                self.to_field = relation.to_field
                self.to_many = relation.to_many
            elif field := model_info.fields.get(self.field.source):
                self.model_field = field


class SerializerSchema(dict):
    def __init__(self, serializer):
        self.serializer = serializer
        meta = getattr(serializer, "Meta", None)
        self.model = getattr(meta, "model", None)

        self.update(self.build_schema())

    def build_schema(self):
        return {
            fieldname: self.build_field(fieldname, field)
            for fieldname, field in self.serializer.fields.items()
        }

    def build_field(self, fieldname, field):
        return FieldSchema(fieldname, field, self)


class AutoSchema(ViewInspector):
    def serializer_schema(self, path, method):
        return SerializerSchema(self.view.get_serializer())

    def allows_filters(self, path, method):
        if getattr(self.view, "filter_backends", None) is None:
            return False
        if hasattr(self.view, "action"):
            return self.view.action in [
                "list",
                "retrieve",
                "update",
                "partial_update",
                "destroy",
            ]

    def filter_parameters(self, path, method):
        if not self.allows_filters(path, method):
            return []
        parameters = []
        for filter_backend in self.view.filter_backends:
            parameters += filter_backend().get_schema_operation_parameters(self.view)
        return parameters
