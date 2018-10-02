from django.db.models import fields
from django.db.models.fields import related
from django.utils.text import mark_safe
from django.db.models import ForeignKey, OneToOneField, ManyToManyField


def get_serializer_field(field):
    if type(field) in [ForeignKey, OneToOneField, ManyToManyField]:
        args = [
            f'source = "{field.name}"',
        ]
        if isinstance(field, ManyToManyField):
            args.append('many = True')
            args.append('read_only = True')

        return f'{field.name}_obj = {field.related_model.__name__}Serializer({",".join(args)})\n    '

    return ''


def get_serializer_string_field(field):
    if type(field) in [ForeignKey, OneToOneField, ManyToManyField]:
        return f'"{field.name}",\n            "{field.name}_obj",'
    return f'"{field.name}",'
