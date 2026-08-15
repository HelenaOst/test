"""
Серіалізатори для брендів і моделей автомобілів
"""
from rest_framework import serializers

from apps.cars.models import Brand, CarModel


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')
        read_only_fields = ('id',)

class CarModelReadSerializer(serializers.ModelSerializer):
    """Для читання: повні дані бренду + модель."""
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = CarModel
        fields = ['id', 'brand', 'name']

class CarModelWriteSerializer(serializers.ModelSerializer):
    """Для запису: тільки ID бренду."""
    class Meta:
        model = CarModel
        fields = ['id', 'brand', 'name']
        read_only_fields = ('id',)

class SendEmailSerializer(serializers.Serializer):
    """Серіалізатор для відправки повідомлення на email."""
    message = serializers.CharField(
        max_length=1000,
        trim_whitespace=True,
    )