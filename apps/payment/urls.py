from django.urls import path

from apps.payment.views import CurrencyRateView

urlpatterns = [
    # Ендпоінт доступу до курсів валют
    path('rate/', CurrencyRateView.as_view(), name='payment')
]
