from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.cars.models import Brand, CarModel
from apps.cars.serializers import BrandSerializer, CarModelReadSerializer, CarModelWriteSerializer, SendEmailSerializer
from apps.core.permissions.permissions import HasPermissionCodenameOrReadOnly

# Create your views here.

class CarModelListCreateView(ListCreateAPIView):
    queryset = CarModel.objects.all()
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_add_car_models'

    #метод обрання сріалайзеру
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarModelReadSerializer
        return CarModelWriteSerializer

class CarModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_update_delete_car_models'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarModelReadSerializer
        return CarModelWriteSerializer


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_add_brands'

class BrandDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_update_delete_brands'

class CarModelByBrandView(ListAPIView):
    serializer_class = CarModelReadSerializer

    def get_queryset(self):
        pk=self.kwargs['pk']
        return CarModel.objects.filter(brand_id=pk)

class BrandEmailView(GenericAPIView):
    serializer_class = SendEmailSerializer
