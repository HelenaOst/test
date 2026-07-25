from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from apps.core.permissions.permissions import HasPermissionCodename, IsOwner
from apps.listing.models import Listing
from apps.listing_stats.serializers import ListingStatsSerializer
from apps.listing_stats.services import ListingStatsService


# Create your views here.
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



