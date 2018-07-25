from django.template import Library
from vqapps.mediamanager.models import Media

from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results
register = Library()


@register.inclusion_tag("admin/mediamanager/change_list_results.html")
def mediamanager_result_list(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl)),
            'opts': Media._meta}


@register.inclusion_tag("admin/mediamanager/folder_select.html")
def folder_select():
    return {
        'folders': list(Media.FOLDER_CHOICES)
    }
