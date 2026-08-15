"""
URL конфігурація для проекту.

Підключає:
- Swagger/ReDoc документацію API
- Додатки: auth, users, cars, listings, payment, statistics
"""

from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Адмінка Django
    path('admin/', admin.site.urls),

    # ========== API ДОКУМЕНТАЦІЯ ==========
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ========== ЕНДПОІНТИ ДОДАТКІВ ==========
    path("api/auth/", include('apps.auth.urls')),
    path("api/users/", include('apps.users.urls')),
    path("api/cars/", include('apps.cars.urls')),
    path("api/listings/", include('apps.listing.urls')),
    path('api/listings/statistics/', include('apps.listing_stats.urls')),
    path('api/payment/', include('apps.payment.urls')),
]