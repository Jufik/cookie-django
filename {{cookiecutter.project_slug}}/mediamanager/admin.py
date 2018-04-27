from django.contrib import admin
from mediamanager.models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    '''Admin View for Media'''

    list_display = ['filename', 'content_type', 'author']
    list_filter = ['content_type']
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ['']
    # readonly_fields = ['']
    search_fields = ['filename']
    # date_hierarchy = ''
    # ordering = ['']