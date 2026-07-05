import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from apps.core.permissions.permissions import HasPermissionCodename
from apps.users.models import Profile, Role
from apps.users.serializers import ProfileUpgradeSerializer, UserProfileUpdateSerializer, UserReadSerializer

UserModel = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = UserModel.objects.select_related('profile', 'role').filter(deleted_at__isnull=True).all()
    serializer_class = UserReadSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_view_users'


class UserDetailView(generics.RetrieveAPIView):
    queryset = UserModel.objects.select_related('profile', 'role').all()
    serializer_class = UserReadSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_view_user_by_id'


class UserDeleteView(generics.DestroyAPIView):
    queryset = UserModel.objects.select_related('profile', 'role').filter(deleted_at__isnull=True)
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_delete_user_by_id'

    def destroy(self, *args, **kwargs):
        user = self.get_object()


        #щоб не видалити себе
        if user == self.request.user:
            return Response(
                {'message': 'You cannot delete yourself.'},
                status=status.HTTP_403_FORBIDDEN
            )

        #щоб не видалити адміна
        if user.is_superuser or (user.role and user.role.name == 'admin'):
            return Response(
                {'message': 'You cannot delete admin.'},
                status=status.HTTP_403_FORBIDDEN
            )


        user.soft_delete()
        return Response(
            {'message': 'User account has been deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )


class UserMeView(generics.RetrieveAPIView):
    permission_classes = [HasPermissionCodename]
    serializer_class = UserReadSerializer
    required_permission = 'can_view_own_account'

    def get_object(self):
        return self.request.user


class UserMeUpdateView(generics.UpdateAPIView):
    permission_classes = [HasPermissionCodename]
    serializer_class = UserProfileUpdateSerializer
    required_permission = 'can_update_own_account'

    def get_object(self):
        return self.request.user


class UserMeDeleteView(generics.DestroyAPIView):
    permission_classes = [HasPermissionCodename]
    serializer_class = UserProfileUpdateSerializer
    required_permission = 'can_delete_own_account'

    def get_object(self):
        return self.request.user

    # soft delete
    def destroy(self, *args, **kwargs):
        user = self.get_object()
        user.soft_delete()
        return Response(
            {'message': 'User account has been deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )


class UserBlockView(GenericAPIView):
    queryset = UserModel.objects.select_related('profile', 'role').all()
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_block_unblock_user'

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        # менеджер не блоконе тепер себе
        if user == request.user:
            return Response(
                {'message': 'You cannot block yourself.'},
                status=status.HTTP_403_FORBIDDEN
            )
        # щоб не був заблокований адмін
        if user.is_superuser or (user.role and user.role.name == 'admin'):
            return Response(
                {'message': 'You cannot block admin.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])

        status_text = 'blocked' if not user.is_active else 'unblocked'
        return Response(
            {
                'message': f'User has been {status_text}.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_active': user.is_active,
                    'profile': {
                        'name': user.profile.name if user.profile else None,
                        'type': user.profile.type_profile if user.profile else None,
                        'account_type': user.profile.account_type if user.profile else None,
                    }
                }
            },
            status=status.HTTP_200_OK
        )


class UserToManagerView(GenericAPIView):
    queryset = UserModel.objects.select_related('profile', 'role').all()
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_create_manager'

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        manager_role = get_object_or_404(Role, name='manager')
        user.role = manager_role
        user.save()
        serializer = UserReadSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserToPremiumView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [HasPermissionCodename]
    required_permission = 'can_be_premium_user'
    serializer_class = ProfileUpgradeSerializer

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile_id)



    def perform_update(self, serializer):
        now = timezone.now()
        next_month = now + datetime.timedelta(days=30)

        serializer.save(
            account_type='premium',
            account_expires_at=next_month
        )