from rest_framework.serializers import (
    ModelSerializer as BaseModelSerializer,
    SerializerMetaclass as BaseSerializerMetaclass,
)
import copy

from collections import OrderedDict

from rest_framework.settings import api_settings
from rest_framework.utils import model_meta


class ModelSerializerMetaClass(BaseSerializerMetaclass):
    def __new__(cls, name, bases, attrs):
        instanciated = super().__new__(cls, name, bases, attrs)
        if hasattr(instanciated, "Meta"):
            instanciated.Meta.model.Api.register_serializer(instanciated)
        return instanciated


class ModelSerializer(BaseModelSerializer, metaclass=ModelSerializerMetaClass):
    pass
    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(*args, **kwargs)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.Meta.model.Api.register_serializer(self.__class__)
