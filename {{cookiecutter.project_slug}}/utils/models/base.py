from django.utils.translation import gettext as _
from django.db import models
from .fields import DateTimeField

resources = {}


class BaseModel(models.Model):
    created_at = DateTimeField(_("Creation Date"), auto_now_add=True)
    updated_at = DateTimeField(_("Updated At"), auto_now=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, "display_name"):
            return self.display_name
        if hasattr(self, "name"):
            return self.name
        return super().__str__()

