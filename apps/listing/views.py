from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from apps.core.permissions.permissions import HasPermissionCodename, IsImageOwner, IsOwner
from apps.listing.models import CarImage, Listing, Region
from apps.listing.serializers import (
    ImageSerializer,
    ImageUploadSerializer,
    ListingModerationSerializer,
    ListingReadSerializer,
    ListingWriteSerializer,
    RegionSerializer,
)
from apps.listing_stats.models import ListingStats
from apps.listing_stats.serializers import ListingStatsSerializer

# PUBLIC VIEWS

class ListingsListView(ListAPIView):
    queryset = Listing.objects.filter(status='active')
    serializer_class = ListingReadSerializer


class ListingView(RetrieveAPIView):
    queryset = Listing.objects.filter(status='active')
    serializer_class = ListingReadSerializer


class RegionsListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


# SELLER VIEWS
class MyListingsListView(ListAPIView):
    serializer_class = ListingReadSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_view_own_listings'

    def get_queryset(self):
        queryset = Listing.objects.filter(
            owner=self.request.user,
        )

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset


class ListingCreateView(CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingWriteSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_create_listing'


class ListingUpdateView(UpdateAPIView):
    queryset = Listing.objects.filter(status__in=['active', 'rejected'])
    serializer_class = ListingWriteSerializer
    permission_classes = [HasPermissionCodename, IsOwner]
    required_permission = 'can_update_own_listing'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.edit_count >= 3 and instance.status == 'rejected':
            instance.status = 'inactive'
            instance.save(update_fields=['status'])
            return Response(
                {'message': 'Listing has been blocked.',
                 'listing': self.get_serializer(instance).data
                 },
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if instance.status == 'rejected':
            serializer.save(
                edit_count=instance.edit_count + 1,
                status='pending'
            )
        else:
            serializer.save()
        return Response(
            {
                'message': 'Listing has been updated.',
                'listing': serializer.data
            },
            status=status.HTTP_200_OK
        )


class ListingDeleteView(DestroyAPIView):
    queryset = Listing.objects.filter(status__in=['active', 'rejected', 'pending'])
    serializer_class = ListingWriteSerializer
    permission_classes = [HasPermissionCodename, IsOwner]
    required_permission = 'can_delete_own_listing'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'inactive'
        instance.save(update_fields=['status'])
        return Response(
            {'message': 'Listing has been deactivated.',
             'listing': self.get_serializer(instance).data},
            status=status.HTTP_200_OK
        )


class ImagesUploadView(CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [HasPermissionCodename, IsOwner]
    required_permission = 'can_upload_own_images'

    # виклик вручну get_object() для перевірки власника
    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.get_object())
        serializer.save()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['listing_id'] = self.kwargs['pk']
        return context

    def create(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.save()
        return Response(
            {
                'message': 'Images uploaded successfully.',
                'images': ImageSerializer(images, many=True).data
            },
            status=status.HTTP_201_CREATED
        )


class ImageDeleteView(DestroyAPIView):
    queryset = CarImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [HasPermissionCodename, IsImageOwner]
    required_permission = 'can_delete_own_images'

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        photo = self.get_object()
        photo.delete()
        return Response(
            {'message': 'Image has been deleted.'},
            status=status.HTTP_200_OK
        )


# MANAGER VIEWS
class PendingListingsListView(ListAPIView):
    queryset = Listing.objects.filter(status='pending')
    serializer_class = ListingReadSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_edit_listings'


class ModeratingListingView(UpdateAPIView):
    queryset = Listing.objects.filter(status='pending')
    serializer_class = ListingModerationSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_moderate_listings'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Listing has been moderated.',
             'listing': serializer.data
             },
            status=status.HTTP_200_OK
        )


# PREMIUM SELLER VIEWS
class ListingStatsView(RetrieveAPIView):
    queryset = ListingStats.objects.all()
    serializer_class = ListingStatsSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_view_statistics'
