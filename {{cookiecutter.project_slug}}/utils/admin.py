from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.admin.widgets import (
    AutocompleteSelect,
    AutocompleteSelectMultiple,
)
from django.utils.http import urlencode
from urllib.parse import unquote, quote_plus, parse_qsl


class AutocompleteUrl(object):
    def get_url(self):
        url = super().get_url()
        return url + "?" + urlencode(self.filters)

    def __init__(self, *args, **kwargs):
        self.filters = kwargs.pop("filters", {})
        super().__init__(*args, **kwargs)


class ManyToManyAutocompleteSelect(AutocompleteUrl, AutocompleteSelectMultiple):
    pass


class ForeignKeyAutocompleteSelect(AutocompleteUrl, AutocompleteSelect):
    pass


class LimitAutocompleteJsonView(AutocompleteJsonView):
    # Filter the results with the arguments passed to the url
    def get_queryset(self,request=None):
        qs = super().get_queryset()
        filters = self.request.GET.dict()

        if not filters:
            return qs
        return qs.filter(**filters)


class HelperAdmin(BaseModelAdmin):
    limit_choices_fields = []

    def get_filters(self, request):
        return {}

    def autocomplete_view(self, request):
        return LimitAutocompleteJsonView.as_view(model_admin=self)(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.limit_choices_fields:
            db = kwargs.get("using")
            kwargs["widget"] = ForeignKeyAutocompleteSelect(
                db_field.remote_field,
                self.admin_site,
                using=db,
                **{"filters": self.get_filters(request)},
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in self.limit_choices_fields:
            db = kwargs.get("using")
            kwargs["widget"] = ManyToManyAutocompleteSelect(
                db_field.remote_field,
                self.admin_site,
                using=db,
                **{"filters": self.get_filters(request)},
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)
