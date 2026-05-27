from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.permissions import IsAdmin, IsAdminOrManager, IsManager, IsSuperUser
from apps.users.serializers import UserProfileUpdateSerializer, UserReadSerializer

UserModel = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = UserModel.objects.select_related('profile', 'role').all()
    serializer_class = UserReadSerializer
    permission_classes = [IsAdmin | IsManager]


class UserDetailView(generics.RetrieveDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsAdmin | IsManager]


class UserMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserReadSerializer
        return UserProfileUpdateSerializer


class UserBlockView(GenericAPIView):
    permission_classes = [IsAdmin | IsManager]

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()

        serializer = UserReadSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        admin_role=Role.objects.get(name='admin')
        user.role = admin_role
        user.save()
        serializer = UserReadSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
