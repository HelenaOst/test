from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.cars.models import Brand, CarModel
from apps.core.models import BaseModel
from apps.users.models import User


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Listing(BaseModel):
    class CarConditions(models.TextChoices):
        NEW = 'new', 'Новий'
        USED = 'used', 'Вживаний'

    class BodyType(models.TextChoices):
        SEDAN = 'sedan', 'Седан'
        SUV = 'suv', 'Позашляховик'
        HATCHBACK = 'hatchback', 'Хетчбек'
        COUPE = 'coupe', 'Купе'
        WAGON = 'wagon', 'Універсал'
        PICKUP = 'pickup', 'Пікап'
        VAN = 'van', 'Мінівен'
        CABRIO = 'cabrio', 'Кабріолет'

    class FuelType(models.TextChoices):
        PETROL = 'petrol', 'Бензин'
        DIESEL = 'diesel', 'Дизель'
        HYBRID = 'hybrid', 'Гібрид'
        ELECTRIC = 'electric', 'Електричний'
        GAS = 'gas', 'Газ'

    class TransmissionType(models.TextChoices):
        MANUAL = 'manual', 'Механіка'
        AUTOMATIC = 'automatic', 'Автомат'
        ROBOT = 'robot', 'Робот'
        CVT = 'cvt', 'Варіатор'

    class DriveType(models.TextChoices):
        FWD = 'fwd', 'Передній привід'
        RWD = 'rwd', 'Задній привід'
        AWD = 'awd', 'Повний привід'

    class CurrencyType(models.TextChoices):
        USD = 'USD', 'Долар США'
        EUR = 'EUR', 'Євро'
        UAH = 'UAH', 'Гривня'

    class ListingStatus(models.TextChoices):
        ACTIVE = 'active', 'Активне'
        PENDING = 'pending', 'На перевірці'
        REJECTED = 'rejected', 'Відхилено'
        BLOCKED = 'blocked', 'Заблоковано'

    # characteristics
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="listings")

    color = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")

    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 1)
        ]
    )
    mileage = models.PositiveIntegerField(help_text='Mileage in kilometers')
    engine_volume = models.DecimalField(max_digits=4, decimal_places=1)
    condition_type = models.CharField(max_length=20, choices=CarConditions)
    body_type = models.CharField(max_length=20, choices=BodyType)
    fuel_type = models.CharField(max_length=20, choices=FuelType)
    transmission_type = models.CharField(max_length=20, choices=TransmissionType)
    drive_type = models.CharField(max_length=20, choices=DriveType)
    description = models.TextField(blank=True)

    # price
    currency = models.CharField(max_length=10, choices=CurrencyType)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_uah = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # listing status
    listing_status = models.CharField(max_length=10, choices=ListingStatus, default=ListingStatus.PENDING)

    # edit counter
    edit_count = models.PositiveIntegerField(default=0)
    moderation_count = models.PositiveIntegerField(default=0)

    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_model.brand} {self.car_model} {self.year}"


class CarImages(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="car_images")
    image = models.ImageField(upload_to='listing_images')
    is_main = models.BooleanField(default=False)

