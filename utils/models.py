from django.db import models


class TimeStampModel(models.Model):
    """
    Gives usual publishable TimeStamp field and Managers
    """
    created_at = models.DateTimeField(verbose_name="Création", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Mise à jour", auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True