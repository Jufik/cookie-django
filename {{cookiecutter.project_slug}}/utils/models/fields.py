from django.db.models.fields import (
    AutoField as BaseAutoField,
    BigAutoField as BaseBigAutoField,
    BigIntegerField as BaseBigIntegerField,
    BinaryField as BaseBinaryField,
    BooleanField as BaseBooleanField,
    CharField as BaseCharField,
    CommaSeparatedIntegerField as BaseCommaSeparatedIntegerField,
    DateField as BaseDateField,
    DateTimeField as BaseDateTimeField,
    DecimalField as BaseDecimalField,
    DurationField as BaseDurationField,
    EmailField as BaseEmailField,
    Field,
    FilePathField as BaseFilePathField,
    FloatField as BaseFloatField,
    GenericIPAddressField as BaseGenericIPAddressField,
    IPAddressField as BaseIPAddressField,
    IntegerField as BaseIntegerField,
    NullBooleanField as BaseNullBooleanField,
    PositiveBigIntegerField as BasePositiveBigIntegerField,
    PositiveIntegerField as BasePositiveIntegerField,
    PositiveSmallIntegerField as BasePositiveSmallIntegerField,
    SlugField as BaseSlugField,
    SmallAutoField as BaseSmallAutoField,
    SmallIntegerField as BaseSmallIntegerField,
    TextField as BaseTextField,
    TimeField as BaseTimeField,
    URLField as BaseURLField,
    UUIDField as BaseUUIDField,
)
from django.db.models.fields.files import (
    FileField as BaseFileField,
    ImageField as BaseImageField,
)
from django.db.models.fields.json import JSONField as BaseJSONField


from django.db.models.fields.related import (  # isort:skip
    ForeignKey as BaseForeignKey,
    OneToOneField as BaseOneToOneField,
    ManyToManyField as BaseManyToManyField,
)

__all__ = [
    "AutoField",
    "BigAutoField",
    "BigIntegerField",
    "BinaryField",
    "BooleanField",
    "CharField",
    "FileField",
    "ImageField",
    "CommaSeparatedIntegerField",
    "DateField",
    "ForeignKey",
    "ManyToManyField",
    "OneToOneField",
    "JSONField",
    "DateTimeField",
    "DecimalField",
    "DurationField",
    "EmailField",
    "FilePathField",
    "FloatField",
    "GenericIPAddressField",
    "IPAddressField",
    "IntegerField",
    "NullBooleanField",
    "PositiveBigIntegerField",
    "PositiveIntegerField",
    "PositiveSmallIntegerField",
    "SlugField",
    "SmallAutoField",
    "SmallIntegerField",
    "TextField",
    "TimeField",
    "URLField",
    "UUIDField",
]


def mixin_factory(*args, **kwargs):
    class SerializerClassMixin(Field):
        def __init__(self, *_args, **_kwargs):
            for key, default in kwargs.items():
                setattr(self, key, _kwargs.pop(key, default))
            super().__init__(*_args, **_kwargs)

    return SerializerClassMixin


def add_field_params(FieldClass, *args, **kwargs):
    cls_name = FieldClass.__name__
    return type(cls_name, (mixin_factory(*args, **kwargs), FieldClass), {})


serializer_kwargs = {"serializers": {"light": None, "default": None}}

AutoField = add_field_params(BaseAutoField, **serializer_kwargs)
BigAutoField = add_field_params(BaseBigAutoField, **serializer_kwargs)
BigIntegerField = add_field_params(BaseBigIntegerField, **serializer_kwargs)
BinaryField = add_field_params(BaseBinaryField, **serializer_kwargs)
BooleanField = add_field_params(BaseBooleanField, **serializer_kwargs)
CharField = add_field_params(BaseCharField, **serializer_kwargs)
CommaSeparatedIntegerField = add_field_params(
    BaseCommaSeparatedIntegerField, **serializer_kwargs
)
DateField = add_field_params(BaseDateField, **serializer_kwargs)
DateTimeField = add_field_params(BaseDateTimeField, **serializer_kwargs)
DecimalField = add_field_params(BaseDecimalField, **serializer_kwargs)
DurationField = add_field_params(BaseDurationField, **serializer_kwargs)
EmailField = add_field_params(BaseEmailField, **serializer_kwargs)
FilePathField = add_field_params(BaseFilePathField, **serializer_kwargs)
FloatField = add_field_params(BaseFloatField, **serializer_kwargs)
GenericIPAddressField = add_field_params(BaseGenericIPAddressField, **serializer_kwargs)
IPAddressField = add_field_params(BaseIPAddressField, **serializer_kwargs)
IntegerField = add_field_params(BaseIntegerField, **serializer_kwargs)
NullBooleanField = add_field_params(BaseNullBooleanField, **serializer_kwargs)
PositiveBigIntegerField = add_field_params(
    BasePositiveBigIntegerField, **serializer_kwargs
)
PositiveIntegerField = add_field_params(BasePositiveIntegerField, **serializer_kwargs)
PositiveSmallIntegerField = add_field_params(
    BasePositiveSmallIntegerField, **serializer_kwargs
)
SlugField = add_field_params(BaseSlugField, **serializer_kwargs)
SmallAutoField = add_field_params(BaseSmallAutoField, **serializer_kwargs)
SmallIntegerField = add_field_params(BaseSmallIntegerField, **serializer_kwargs)
TextField = add_field_params(BaseTextField, **serializer_kwargs)
TimeField = add_field_params(BaseTimeField, **serializer_kwargs)
URLField = add_field_params(BaseURLField, **serializer_kwargs)
UUIDField = add_field_params(BaseUUIDField, **serializer_kwargs)
JSONField = add_field_params(BaseJSONField, **serializer_kwargs)
FileField = add_field_params(BaseFileField, **serializer_kwargs)
ImageField = add_field_params(BaseImageField, **serializer_kwargs)


ForeignKey = add_field_params(
    BaseForeignKey,
    **{
        "serializers": {"default": "light", "light": None},
        "related_serializers": {"default": "light"},
    }
)
ManyToManyField = add_field_params(
    BaseManyToManyField,
    **{
        "serializers": {"default": "light", "light": None},
        "related_serializers": {"default": "light"},
    }
)
OneToOneField = add_field_params(
    BaseOneToOneField,
    **{
        "serializers": {"default": "light", "light": None},
        "related_serializers": {"default": "light"},
    }
)

