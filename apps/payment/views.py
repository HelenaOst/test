from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny

from apps.payment.models import CurrencyRate
from apps.payment.serializer import CurrencyRateSerializer


# Create your views here.
class CurrencyRateView(RetrieveAPIView):
    queryset = CurrencyRate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CurrencyRateSerializer

    def get_object(self):
        return get_object_or_404(
            CurrencyRate.objects.order_by('-date')
        )
