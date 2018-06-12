import os
import string
import random

from django.db import models
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from model_utils.models import TimeStampedModel


def normalize_filename(filename):
    # we had a suffix to ensure file unicity
    suffix = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(4))
    arr = filename.split('.')
    ext = arr[-1]
    filename = ('-'.join(arr[:-1])).lower()
    filename = f"{filename}-{suffix}.{ext}"
    return filename

def media_images_upload_to(instance, filename):
    filename = normalize_filename(filename)
    return os.path.join('medias', instance.folder, filename)

def media_files_upload_to(instance, filename):
    filename = normalize_filename(filename)
    return os.path.join('files', instance.folder, filename)


class Media(TimeStampedModel):
    PRODUCT_FOLDER = 'products'
    FOLDER_CHOICES = (
        (PRODUCT_FOLDER, PRODUCT_FOLDER,),
    )
    MEDIA_IMAGE = 0
    MEDIA_ATTACHMENT = 1
    MEDIA_TYPE_CHOICES = (
        (MEDIA_IMAGE, 'Image',),
        (MEDIA_ATTACHMENT, 'Attachment',)
    )
    folder = models.CharField('Folder', max_length=50, choices=FOLDER_CHOICES)
    filename = models.CharField('Name', max_length=255, editable=False)
    description = models.CharField('description (for SEO)', max_length=255, blank=True)
    media_type = models.PositiveSmallIntegerField(choices=MEDIA_TYPE_CHOICES, editable=False)
    content_type = models.CharField('Content Type', max_length=255, editable=False)
    image = models.ImageField(upload_to=media_images_upload_to, verbose_name="Image", blank=True, null=True)
    attachment = models.FileField(upload_to=media_files_upload_to, verbose_name="Fichier", blank=True, null=True)
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

    def clean(self, *args, **kwargs):
        super(Media, self).clean(*args, **kwargs)
        from django.core.exceptions import ValidationError
        if not bool(self.attachment) and not bool(self.image):
            raise ValidationError({
                'image': 'you must set an attachment or an image',
                'attachment': 'you must set an attachment or an image'
            })
        if bool(self.attachment) and bool(self.image):
            raise ValidationError({
                'image': 'you must set an attachment or an image, not both',
                'attachment': 'you must set an attachment or an image, not both'
            })

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
    
    @property
    def ext(self):
        return self.filename.split('.')[-1]

    def get_media_type(self):
        if self.attachment:
            return self.MEDIA_ATTACHMENT
        elif self.image:
            return self.MEDIA_IMAGE
        else:
            return None
    
    def set_media_type(self, commit=False):
        self.media_type = self.get_media_type()
        if commit:
            super(Media, self).save()

    def get_filename(self):
        if self.is_attachment:
            return os.path.basename(self.attachment.name)
        elif self.is_image:
            return os.path.basename(self.image.name)
        else:
            return None
    
    def set_filename(self, commit=False):
        self.filename = self.get_filename()
        if commit:
            super(Media, self).save()

    def get_content_type(self):
        if self.is_attachment:
            return self.attachment.file.content_type
        elif self.is_image:
            return self.image.file.content_type
        else:
            return None

    def set_content_type(self, commit=False):
        self.content_type = self.get_content_type()
        if commit:
            super(Media, self).save()

    @property
    def is_attachment(self):
        return self.media_type == self.MEDIA_ATTACHMENT

    @property
    def is_image(self):
        return self.media_type == self.MEDIA_IMAGE

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_media_type()
            self.set_filename()
            self.set_content_type()
        super(Media, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.is_attachment:
            self.attachment.delete(False)
        if self.is_image:
            self.image.delete(False)
        super(Media, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medias"
        app_label = 'mediamanager'

    def __str__(self):
        return self.filename
