from django.urls import path

from apps.cars.views import (
    BrandDetailView,
    BrandListCreateView,
    CarModelByBrandView,
    CarModelDetailView,
    CarModelListCreateView,
)

urlpatterns = [
    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand-detail'),
    path('models/', CarModelListCreateView.as_view(), name='carmodel-list-create'),
    path('models/<int:pk>/', CarModelDetailView.as_view(), name='carmodel-detail'),
    path('brands/<int:pk>/models/', CarModelByBrandView.as_view(), name='brand-models-list-create'),
]