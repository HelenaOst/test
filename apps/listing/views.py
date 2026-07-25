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
from apps.listing.tasks import update_one_listing_prices_task
from apps.listing_stats.models import ListingStats
from apps.moderation.services import EmailForModeration
from apps.moderation.tasks import moderation_listings_task

# PUBLIC VIEWS

class ListingsListView(ListAPIView):
    queryset = Listing.objects.filter(status='active')
    serializer_class = ListingReadSerializer


class ListingView(RetrieveAPIView):
    queryset = Listing.objects.filter(status='active')
    serializer_class = ListingReadSerializer

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        if not request.user.is_authenticated or request.user != listing.owner:
            ListingStats.objects.create(
                listing=listing,
                viewer=request.user if request.user.is_authenticated else None
            )
        serializer = self.get_serializer(listing)
        return Response(serializer.data)


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

    def perform_create(self, serializer):
        listing = serializer.save()
        moderation_listings_task.delay(listing.id)
        update_one_listing_prices_task.delay(listing.id)


class ListingUpdateView(UpdateAPIView):
    queryset = Listing.objects.filter(status__in=['active', 'rejected'])
    serializer_class = ListingWriteSerializer
    permission_classes = [HasPermissionCodename, IsOwner]
    required_permission = 'can_update_own_listing'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.edit_count >= 2 and instance.status == 'rejected':
            instance.status = 'inactive'
            instance.save(update_fields=['status'])
            EmailForModeration.send_blocked_listing_email(instance)
            return Response(
                {'message': 'Listing has been blocked.',
                 'listing': self.get_serializer(instance).data
                 },
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if instance.status == 'rejected':
            updated = serializer.save(
                edit_count=instance.edit_count + 1,
                status='pending'
            )
        else:
            updated = serializer.save(status='pending')
        moderation_listings_task.delay(updated.id)
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