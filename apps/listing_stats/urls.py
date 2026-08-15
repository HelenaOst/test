from django.urls import path

from apps.listing_stats.views import ListingStatsView

urlpatterns = [
    # Ендпоінт доступу до статистики оголошень
    path('<int:pk>/', ListingStatsView.as_view(), name='statistics'),
]
