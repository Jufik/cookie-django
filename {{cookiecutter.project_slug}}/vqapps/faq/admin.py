from django.contrib import admin

from vqapps.faq.models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    '''Admin View for FAQ'''

    list_display = ('question', 'is_active',)
    list_filter = ('is_active',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('created', 'modified',)
    search_fields = ('question', 'answer',)
    # date_hierarchy = ''
    # ordering = ('',)
