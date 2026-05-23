from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.cars.models import Brand, CarModel
from apps.cars.serializers import BrandSerializer, CarModelReadSerializer, CarModelWriteSerializer


# Create your views here.
class CarModelListCreateView(ListCreateAPIView):
    queryset = CarModel.objects.all()

    #метод обрання сріалайзеру
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarModelReadSerializer
        return CarModelWriteSerializer

class CarModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarModelReadSerializer
        return CarModelWriteSerializer


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CarModelByBrandView(ListCreateAPIView):
    serializer_class = CarModelReadSerializer

    def get_queryset(self):
        pk=self.kwargs['pk']
        return CarModel.objects.filter(brand_id=pk)