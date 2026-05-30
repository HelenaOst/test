from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from apps.users.models import Profile, Role

UserModel = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=['buyer', 'seller'],
        write_only=True
    )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role_name = validated_data.pop('role', 'buyer')

        with transaction.atomic():
            user = UserModel.objects.create_user(
                email=validated_data['email'],
                username=validated_data['email'],
                password=validated_data['password'],
                phone=validated_data['phone'],
            )
            user.role = Role.objects.get(name=role_name)

            # створюємо профіль і прив'язуємо до юзера
            profile = Profile.objects.create(name=validated_data['email'])
            user.profile = profile

            user.save(update_fields=['role', 'profile'])
        return user