from django.db import models

from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel


class FAQ(OrderedModel, TimeStampedModel):
    """
    Model definition for FAQ.
    """

    question = models.CharField(verbose_name='Question', max_length=255)
    answer = models.TextField(verbose_name='Answer')
    is_active = models.BooleanField(verbose_name='Is Active ?', default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
    
    def save(self, *args, **kwargs):
        super(FAQ, self).save(*args, **kwargs)