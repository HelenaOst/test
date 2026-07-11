from django.urls import path

from apps.payment.views import PaymentView

urlpatterns = [
    path('rate/', PaymentView.as_view(), name='payment')
]
