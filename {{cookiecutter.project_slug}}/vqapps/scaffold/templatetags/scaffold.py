from django import template
from vqapps.scaffold.factory_helpers import get_factory_field as factory_field
from vqapps.scaffold.serializer_helpers import (get_serializer_field as serializer_field,
                                                get_serializer_string_field as serializer_string_field
                                                )
from django.db.models import ForeignKey, OneToOneField, ManyToManyField
register = template.Library()


@register.filter
def get_model_classname(model):
    return model.__class__.__name__


@register.filter
def get_fields(model):
    return model._meta.fields + model._meta.many_to_many


@register.filter
def get_factory_field(field):
    return factory_field(field)


@register.filter
def get_serializer_field(field):
    return serializer_field(field)


@register.filter
def get_serializer_string_field(field):
    return serializer_string_field(field)


@register.filter
def get_m2m_fields(model):
    return model._meta.many_to_many
