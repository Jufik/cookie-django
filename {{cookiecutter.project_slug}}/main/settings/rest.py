REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.SessionAuthentication',
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 30,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_METADATA_CLASS": "api.metadata.MetaData",
    "DEFAULT_SCHEMA_CLASS": "api.schema.fields.AutoSchema",
    'EXCEPTION_HANDLER': 'utils.views.custom_exception_handler'
}

# Django Cors Headers

CORS_ORIGIN_ALLOW_ALL = True


# Django Rest Auth

LOGOUT_ON_PASSWORD_CHANGE = False
OLD_PASSWORD_FIELD_ENABLED = False
