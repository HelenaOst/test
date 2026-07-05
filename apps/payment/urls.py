from django.urls import path

from apps.payment.views import PaymentView

path('rate/', PaymentView.as_view(), name='payment')
