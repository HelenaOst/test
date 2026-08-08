from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cars.models import Brand, CarModel
from apps.cars.serializers import BrandSerializer, CarModelReadSerializer, CarModelWriteSerializer, SendEmailSerializer
from apps.cars.tasks import send_offer_new_carmodel_task
from apps.core.permissions.permissions import HasPermissionCodenameOrReadOnly

# Create your views here.

class CarModelListCreateView(ListCreateAPIView):
    queryset = CarModel.objects.select_related("brand")
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_add_car_models'

    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = [
        "name",
        "brand__name",
    ]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarModelReadSerializer
        return CarModelWriteSerializer


class CarModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.select_related("brand")
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_update_delete_car_models'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarModelReadSerializer
        return CarModelWriteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {'message': 'CarModel has been deleted.'},
            status=status.HTTP_200_OK
        )


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_add_brands'

    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class BrandDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [HasPermissionCodenameOrReadOnly]
    required_permission = 'can_update_delete_brands'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Brand has been deleted.'},
            status=status.HTTP_200_OK
        )


class CarModelByBrandView(ListAPIView):
    serializer_class = CarModelReadSerializer

    def get_queryset(self):
        get_object_or_404(Brand, pk=self.kwargs["pk"])

        return (
            CarModel.objects
            .filter(brand_id=self.kwargs["pk"])
            .select_related("brand")
        )


class OfferNewCarModelView(GenericAPIView):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_offer_new_carmodel_task.delay(request.user.id, serializer.validated_data['message'])
        return Response(
            {'message': 'Your request has been sent.'},
            status=status.HTTP_200_OK

        )