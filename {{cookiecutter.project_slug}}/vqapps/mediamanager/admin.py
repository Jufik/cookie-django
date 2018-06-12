from django.contrib import admin

from vqapps.mediamanager.models import Media
from vqapps.mediamanager.forms import MediaForm


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    '''Admin View for Media'''

    list_display = ('filename',)
    list_filter = ('content_type', 'media_type', 'folder',)
    form = MediaForm
    # inlines = (
    #     Inline,
    # ]
    # raw_id_fields = ('')
    # readonly_fields = ('')
    actions = []
    search_fields = ('filename', 'description')
    # date_hierarchy = ''
    # ordering = ('')