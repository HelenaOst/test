from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.payment.models import CurrencyRate
from apps.payment.serializer import CurrencyRateSerializer


# Create your views here.
class PaymentView(RetrieveAPIView):
    queryset = CurrencyRate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CurrencyRateSerializer

    def get_object(self):
        return CurrencyRate.objects.latest('date')
