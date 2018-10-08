from django.db.models import fields
from django.db.models.fields import related
from django.utils.text import mark_safe
from django.db.models import ForeignKey, OneToOneField, ManyToManyField


def build_dependencies(app, models):
    res = {}
    # Get all "related" app/model from models fields, that are not already in "app"
    # This can be duplicated
    # for a in models[0]._meta.many_to_many:
    #     print(dir(a))
    related_models = [(field.related_model._meta.app_label, field.related_model.__name__) for model in models for field in model._meta.fields + model._meta.many_to_many if (
        type(field) in [ForeignKey, OneToOneField, ManyToManyField] and
        field.related_model._meta.app_label != app)]
    for app, model in related_models:
        if app in res:
            res[app].add(model)
        else:
            res[app] = set([model])
    return res



def get_factory_field(field):
    """
    This method intend to give
    """

    # if field.default != fields.NOT_PROVIDED:
    #     return f'# skipped field {field.name} ({field.__class__.__name__}) with default value ({field.default})'

    # if field.blank or field.null:
    #     return f'# skipped blank or nullable {field.name}'
    if field.name in ['is_deleted', 'is_active', 'created_at', 'updated_at']:
        return f'# skipped {field.name}'

    if field.choices:
        choices = ",".join(["\'%s\'" % a[0] for a in field.choices])
        return f'{field.name} = factory.fuzzy.FuzzyChoice([{choices}])'
    if isinstance(field, fields.IntegerField):
        return f'{field.name} = factory.fuzzy.FuzzyInteger()'

    if isinstance(field, fields.EmailField):
        return f'{field.name} = factory.Faker("email")'

    if isinstance(field, fields.BooleanField):
        return f'{field.name} = factory.Faker("pybool")'
    if isinstance(field, fields.CharField) or isinstance(field, fields.TextField):

        if field.name in ['first_name', 'last_name']:
            return f'{field.name} = factory.Faker("{field.name}")'
        elif 'name' in field.name:
            return f'{field.name} = factory.Faker("word")'
        elif 'phone' in field.name:
            return f'{field.name} = factory.Faker("phone_number", locale="fr_FR")'
        elif 'comment' in field.name:
            return f'{field.name} = factory.Faker("sentence")'
        elif 'description' in field.name:
            return f'{field.name} = factory.Faker("sentence")'

        else:
            return f'#{field.name} = factory.Faker("lexify", text="??????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")'

    if isinstance(field, fields.DateTimeField):
        return f'{field.name} = factory.fuzzy.FuzzyNaiveDateTime()'

    if isinstance(field, fields.DateField):
        return f'{field.name} = factory.fuzzy.FuzzyDate()'

    if type(field) in [ForeignKey, OneToOneField, ManyToManyField]:
        return f'{field.name} = factory.SubFactory("{field.related_model._meta.app_label}.factory.{field.related_model.__name__}Factory")'

    # TODO
    # if isinstance(field, fields.FloatField):
    #     return f'{field.name} = factory.Faker("sentence")'

    return f'#{field.name} did not find the relevant factory: {mark_safe(type(field))}'
