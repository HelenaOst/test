from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.core.permissions.permissions import HasPermissionCodename, IsOwner
from apps.listing.models import Listing
from apps.listing_stats.serializers import ListingStatsSerializer
from apps.listing_stats.services import ListingStatsService


# Create your views here.
@extend_schema(
    summary="Переглянути статистику",
    description="Дозволяє преміум-користувачам отримувати статистику по власним оголошенням. Інформація доступна менеджерам і адміністраторам"
)
class ListingStatsView(RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingStatsSerializer
    permission_classes = [HasPermissionCodename, IsOwner]
    required_permission = 'can_view_statistics'

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        stats = ListingStatsService.get_stats(listing)
        serializer = self.get_serializer(stats)
        return Response(serializer.data)



