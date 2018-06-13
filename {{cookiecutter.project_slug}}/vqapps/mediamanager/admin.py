import json

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.conf.urls import url
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.admin.utils import unquote

from vqapps.mediamanager.models import Media
from vqapps.mediamanager.forms import MediaForm


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    '''Admin View for Media'''

    list_display = ('filename', 'created',)
    list_filter = ('content_type', 'media_type', 'folder',)
    form = MediaForm
    # inlines = (
    #     Inline,
    # ]
    # raw_id_fields = ('')
    # readonly_fields = ('')
    actions = None
    search_fields = ('filename', 'description')
    # date_hierarchy = ''
    # ordering = ('')

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        return [
            url(
                r'^js/upload$',
                self.admin_site.admin_view(self.media_upload),
                name='media_upload',
            ),
            url(
                r'^(.+)/js/delete$',
                self.admin_site.admin_view(self.media_delete),
                name='media_delete',
            ),
        ] + super(MediaAdmin, self).get_urls()
    
    def media_upload(self, request, form_url=''):
        if request.method != 'POST':
            return HttpResponseNotFound()
        if not (request.user.is_staff and request.user.has_perm('mediamanager.add_media')):
            raise PermissionDenied
        form = MediaForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponseBadRequest(form.errors.as_json())

    def media_delete(self, request, id, form_url=''):
        if request.method != 'POST':
            return HttpResponseNotFound()
        if not (request.user.is_staff and request.user.has_perm('mediamanager.delete_media')):
            raise PermissionDenied
        media = self.get_object(request, unquote(id))
        if media is None:
            return HttpResponseNotFound()
        else:
            media.delete()
            return HttpResponse(status=201)
