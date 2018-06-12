from django.contrib import admin
from vqapps.mediamanager.models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    '''Admin View for Media'''

    list_display = ('filename',)
    list_filter = ('content_type', 'media_type', 'folder',)
    # inlines = (
    #     Inline,
    # ]
    # raw_id_fields = ('')
    # readonly_fields = ('')
    actions = None
    search_fields = ('filename', 'description')
    # date_hierarchy = ''
    # ordering = ('')