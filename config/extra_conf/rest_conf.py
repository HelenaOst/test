REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Тільки JSON
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT токени
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.PagePagination',  # Кастомна пагінація
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',  # Фільтрація
        'rest_framework.filters.SearchFilter',  # Пошук
        'rest_framework.filters.OrderingFilter',  # Сортування
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Генерація OpenAPI схеми
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AutoRia Clone API',
    'DESCRIPTION': 'REST API платформи для продажу автомобілів',
    'VERSION': '1.0.0',
}