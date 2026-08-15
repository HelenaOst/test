from django.db import transaction

from rest_framework import serializers

from apps.users.models import Profile, Role, User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
        read_only_fields = ('id',)


class ProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'logo', 'description', 'type_profile', 'account_type', 'account_expires_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'logo', 'description']

class ProfileUpgradeSerializer(serializers.ModelSerializer):
    """Серіалізатор для оновлення тарифу (basic/premium)."""

    class Meta:
        model = Profile
        fields = ['account_type', 'account_expires_at']
        read_only_fields = fields


class UserReadSerializer(serializers.ModelSerializer):
    """Серіалізатор для читання даних користувача з роллю та профілем."""

    role = RoleSerializer(read_only=True)
    profile = ProfileReadSerializer()

    class Meta:
        model = User
        fields = ['id', 'profile', 'avatar', 'role', 'phone', 'deleted_at']
        read_only_fields = ('id', 'role', 'deleted_at')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для одночасного оновлення користувача та його профілю.
    Приймає avatar, phone та дані профілю.
    """

    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = ['avatar', 'phone', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        with transaction.atomic():
            # Оновлення даних користувача
            instance = super().update(instance, validated_data)

            # Оновлення профілю (часткове оновлення)
            if profile_data and instance.profile:
                profile_serializer = ProfileUpdateSerializer(
                    instance.profile,
                    data=profile_data,
                    partial=True
                )
                profile_serializer.is_valid(raise_exception=True)
                profile_serializer.save()
            return instance
