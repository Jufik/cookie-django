import inspect
from rest_framework.viewsets import GenericViewSet as BaseGenericViewSet
from rest_framework.metadata import SimpleMetadata
from django.core.exceptions import ImproperlyConfigured
from django.db import models


def set_if_none(cls, name, value):
    if not hasattr(cls, name) or getattr(cls, name) is None:
        setattr(cls, name, value)


class SchemaMeta(type):
    def __new__(cls, cls_name, super_classes, attrs):
        initiated_class = super().__new__(cls, cls_name, super_classes, attrs)
        if cls_name == "GenericViewSet":
            return initiated_class

        try:
            meta = attrs.pop("Meta")
        except KeyError:
            raise ImproperlyConfigured("Meta should be defined on %s" % cls_name)

        try:
            model = getattr(meta, "model")
        except AttributeError:
            raise ImproperlyConfigured(
                "Meta in %s should contain at least a model" % cls_name
            )

        if not (inspect.isclass(model) and issubclass(model, models.Model)):
            raise ImproperlyConfigured(
                "model:%s in %s Meta should inherirt from Model" % (model, cls_name)
            )

        try:
            api = getattr(model, "Api")
        except AttributeError:
            raise ImproperlyConfigured(
                "model:%s for %s Meta should declare Api class" % (model, cls_name)
            )

        key = getattr(meta, "key", "default")

        set_if_none(initiated_class, "queryset", model.objects.all())
        set_if_none(initiated_class, "serializer_class", api.get_serializer(key))
        set_if_none(initiated_class, "search_fields", api.search_fields)
        setattr(initiated_class, "api", api)
        setattr(api, "viewset", initiated_class)
        return initiated_class


class GenericViewSet(BaseGenericViewSet, metaclass=SchemaMeta):
    serializer_classes = {}
    querysets = {}
    filterset_classes = {}

    def get_serializer_class(self):
        default = super().get_serializer_class()
        if hasattr(self, "action"):
            return self.serializer_classes.get(self.action, default)
        return default

    def get_queryset(self, request=None):
        default = super().get_queryset()
        if hasattr(self, "action"):
            return self.querysets.get(self.action, default)(request=self.request)
        return default(request=self.request)

    def get_filterset_class(self):
        default = super().get_filterset_class()
        if hasattr(self, "action"):
            return self.filterset_classes.get(self.action, default)
        return default
