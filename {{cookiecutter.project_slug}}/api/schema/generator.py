from collections import defaultdict
from rest_framework.schemas.generators import BaseSchemaGenerator
from api.options import registry
from api.schema.fields import SerializerSchema


class Generator(BaseSchemaGenerator):
    def __init__(self, *args, **kwargs):
        self.resources = {}
        return super().__init__(*args, **kwargs)

    def get_schema(self, request=None, public=False):
        self._initialise_endpoints()
        self._initialise_resources()
        return self.resources

    def _initialise_resources(self):
        for resource_name, api in registry.items():
            viewset = getattr(api, "viewset", None)
            filterset_class = getattr(viewset, "filterset_class", None)
            search_fields = getattr(viewset, "search_fields", [])
            if api.serializer_store.keys():
                self.resources[resource_name] = {
                    "interfaces": {
                        key: SerializerSchema(serializer())
                        for key, serializer in api.serializer_store.items()
                    },
                    "actions": {},
                    "filters": filterset_class.get_fields() if filterset_class else {},
                    "searchable": len(search_fields) > 0,
                }

        _paths, endpoints = self._get_paths_and_endpoints(request=None)
        for path, verb, view in endpoints:
            api = view.Meta.model.Api
            resource_name = api.resource_name
            serializer = view.get_serializer()
            serializer_meta = getattr(serializer, "Meta", None)
            serializer_key = getattr(serializer_meta, "key", None)
            self.resources[resource_name]["actions"][view.action] = {
                "path": path,
                "verb": verb,
                "serializer": serializer_key or SerializerSchema(serializer)
                # "filters": view.schema.filter_parameters(path, verb),
            }

