from django.db import transaction

from rest_framework import serializers

from apps.cars.serializers import CarModelReadSerializer
from apps.listing.models import CarImage, Listing, Region
from apps.users.models import Role


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_main']


class ImageUploadSerializer(serializers.ModelSerializer):
    # Дозволяємо приймати список файлів через ListField
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = CarImage
        fields = ['uploaded_images']

    def create(self, validated_data):
        # ID оголошення з контексту
        listing_id = self.context['listing_id']
        uploaded_images = validated_data.pop('uploaded_images')

        car_images = []
        for index, image in enumerate(uploaded_images):
            # Якщо це перші фото в оголошенні, перше зробити головним за замовчуванням
            is_main = False
            if index == 0 and not CarImage.objects.filter(listing_id=listing_id).exists():
                is_main = True

            car_images.append(
                CarImage(listing_id=listing_id, image=image, is_main=is_main)
            )

        # всі об'єкти в базі одним SQL-запитом
        CarImage.objects.bulk_create(car_images)
        return car_images


class ListingReadSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True, source='car_images')
    car_model = CarModelReadSerializer(read_only=True)
    owner_phone = serializers.CharField(source='owner.phone', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id',
            'owner_id',
            'region',
            'car_model',
            'color',
            'year',
            'mileage',
            'engine_volume',
            'condition_type',
            'body_type',
            'fuel_type',
            'transmission_type',
            'drive_type',
            'description',
            'currency',
            'original_price',
            'price_usd',
            'price_eur',
            'price_uah',
            'status',
            'images',
            'exchange_rate',
            'owner_phone',
        ]


class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'region',
            'car_model',
            'color',
            'year',
            'mileage',
            'engine_volume',
            'condition_type',
            'body_type',
            'fuel_type',
            'transmission_type',
            'drive_type',
            'description',
            'currency',
            'original_price'
        ]

    def create(self, validated_data):
        user = self.context['request'].user

        with transaction.atomic():
            ## перевірка ліміту для базового акаунту
            if user.profile.account_type == 'basic':
                existing = Listing.objects.filter(
                    owner=user,
                    status__in=['active', 'pending']
                ).exists()
                if existing:
                    raise serializers.ValidationError(
                        'Basic account allows only one active listing.'
                    )

        # робимо з покупця продавця при створенні оголошення
        if user.role.name == 'buyer':
            seller_role = Role.objects.get(name='seller')
            user.role = seller_role
            user.save(update_fields=['role'])

            # присвоєння статусу овнера юзеру
        return Listing.objects.create(owner=user, **validated_data)

class ListingModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['status']

class SendReportSerializer(serializers.Serializer):
    message = serializers.CharField()