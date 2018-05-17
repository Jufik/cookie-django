import os
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from model_utils.models import TimeStampedModel


class Media(TimeStampedModel):

    # not used since content_type can be extracted from file
    # 
    # MEDIA_TYPE_IMAGE = 'image'
    # MEDIA_TYPE_FILE = 'file'
    #
    # MEDIA_TYPE_CHOICES = [
    #     [MEDIA_TYPE_IMAGE, 'Image'],
    #     [MEDIA_TYPE_FILE, 'File'],
    # ]
    #
    # media_type = models.CharField('Media Type', choices=MEDIA_TYPE_CHOICES)

    filename = models.CharField('Name', max_length=255, editable=False)
    content_type = models.CharField('Content Type', max_length=255, editable=False)
    image = models.ImageField(upload_to='medias/images', verbose_name="Image", blank=True, null=True)
    attachment = models.FileField(upload_to='medias/files', verbose_name="Fichier", blank=True, null=True)
    author = models.ForeignKey('emailauth.User', verbose_name='Auteur', editable=False, on_delete=models.SET_NULL, blank=True, null=True)
    thumbnail = ImageSpecField(source='image',
                               processors=[
                                   ResizeToFill(200, 200),
                               ],
                               format='JPEG',
                               options={'quality': 72})
    rectangle = ImageSpecField(source='image',
                               processors=[
                                   ResizeToFit(width=1120),
                               ],
                               format='JPEG',
                               options={'quality': 72})

    @property
    def thumbnail_url(self):
        if self.image:
            return self.thumbnail.url
        return None

    @property
    def rectangle_url(self):
        if self.image:
            return self.rectangle.url
        return None

    def get_content_type(self):
        if self.attachment:
            return self.attachment.file.content_type
        elif self.image:
            return self.image.file.content_type
        else:
            return None

    def get_filename(self):
        if self.attachment:
            return os.path.basename(self.attachment.name)
        elif self.image:
            return os.path.basename(self.image.name)
        else:
            return None
    
    def set_filename(self, commit=False):
        self.filename = self.get_filename()
        if commit:
            super(Media, self).save()

    def set_content_type(self, commit=False):
        self.content_type = self.get_content_type()
        if commit:
            super(Media, self).save()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_filename()
            self.set_content_type()
        super(Media, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.attachment:
            self.attachment.delete(False)
        if self.image:
            self.image.delete(False)
        super(Media, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medias"

    def __str__(self):
        return self.filename
