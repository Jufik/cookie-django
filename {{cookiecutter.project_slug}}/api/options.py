from django.db.models.base import ModelBase as BaseModelBase
from django.db.models import Field
from api.serializers import ModelSerializer
from collections import defaultdict
import importlib
from django.utils.translation import activate, deactivate, get_language, ugettext


class Registry(dict):
    pass


registry = Registry()


class AlreadyRegisteredException(Exception):
    pass


class ApiMeta(type):
    def __new__(cls, cls_name, super_classes, attrs):
        if cls_name != "BaseApi":
            return super().__new__(cls, cls_name, super_classes, attrs)()
        else:
            return super().__new__(cls, cls_name, super_classes, attrs)


class BaseApi(metaclass=ApiMeta):
    def __init__(self, *args, **kwargs):
        self.serializer_store = dict()
        self.extra_kwargs = getattr(self, "extra_kwargs", {})

    def contribute_to_class(self, model, name):
        self.model = model
        # try:
        setattr(model, name, self)
        # self.resource_name = getattr(self, "resource_name", self._resource_name)

        registry[self.resource_name] = self

    @property
    def base_name(self):
        lang = get_language()
        deactivate()
        name = ugettext(self.model._meta.verbose_name_plural)
        activate(lang)
        return name

    @property
    def url_name(self):
        return "_".join(self.base_name.lower().split())

    @property
    def resource_name(self):
        return "-".join(self.base_name.lower().split())

    @property
    def url_path(self):
        return self.resource_name

    def fields(self, key="default", remove=[]):
        for field in self.model._meta.get_fields(include_hidden=False):

            name = field.name
            if not name in self.extra_kwargs:
                self.extra_kwargs.update({name: {}})

            extra_kwargs = {}

            if (
                hasattr(field, "many_to_many")
                and hasattr(field, "one_to_many")
                and (field.many_to_many or field.one_to_many)
            ):
                extra_kwargs.update({"many": True})

            model = getattr(field, "related_model", self.model)

            if not isinstance(field, Field):
                field = field.remote_field
                serializer_conf = getattr(field, "related_serializers", {})
                extra_kwargs.update({"read_only": True})

            else:
                serializer_conf = getattr(field, "serializers", {})

            if key in serializer_conf:
                yield name, field, serializer_conf.get(key), model, extra_kwargs

    def get_serializer(
        self, key,
    ):

        if key in self.serializer_store:
            return self.serializer_store.get(key)
        attrs = {}
        _fields = ["pk"]

        serializer_name = f"{self.model.__name__}{key.title()}Serializer"

        for name, field, conf, model, extra_kwargs in self.fields(key):
            self.extra_kwargs[name].update(extra_kwargs)
            _fields.append(name)
            if type(conf) == str:
                serializer = model.Api.get_serializer(conf)
                attrs.update({name: serializer(**extra_kwargs)})
            elif conf is not None:
                attrs.update({name: conf})
        _key = key

        class Meta:
            model = self.model
            fields = _fields
            key = _key

        serializer = type(serializer_name, (ModelSerializer,), {"Meta": Meta, **attrs})
        # self.serializer_store[key] = serializer
        return serializer

    @property
    def search_fields(self):
        return []

    def register_serializer(self, serializer):

        key = (
            getattr(
                serializer.Meta,
                "key",
                serializer.__name__.replace(self.model.__name__, "")
                .replace("Serializer", "")
                .lower(),
            )
            or "default"
        )
        if key in self.serializer_store:
            raise AlreadyRegisteredException(
                f"Serializer with key:{key} is already registered for {self.model.__name__} api"
            )
        else:
            self.serializer_store[key] = serializer

        if not hasattr(serializer.Meta, "key"):
            setattr(serializer.Meta, "key", key)

