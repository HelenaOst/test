from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from rest_framework.exceptions import ValidationError

from apps.cars.models import Brand, CarModel
from apps.core.models import BaseModel
from apps.users.models import User


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

    class Region(models.TextChoices):
        KYIV = 'kyiv', 'Київ'
        KYIV_REGION = 'kyiv_region', 'Київська область'
        KHARKIV = 'kharkiv', 'Харків'
        KHARKIV_REGION = 'kharkiv_region', 'Харківська область'
        ODESA = 'odesa', 'Одеса'
        ODESA_REGION = 'odesa_region', 'Одеська область'
        DNIPRO = 'dnipro', 'Дніпро'
        DNIPRO_REGION = 'dnipro_region', 'Дніпропетровська область'
        LVIV = 'lviv', 'Львів'
        LVIV_REGION = 'lviv_region', 'Львівська область'
        ZAPORIZHZHIA = 'zaporizhzhia', 'Запоріжжя'
        ZAPORIZHZHIA_REGION = 'zaporizhzhia_region', 'Запорізька область'
        VINNYTSIA = 'vinnytsia', 'Вінниця'
        VINNYTSIA_REGION = 'vinnytsia_region', 'Вінницька область'
        POLTAVA = 'poltava', 'Полтава'
        POLTAVA_REGION = 'poltava_region', 'Полтавська область'
        CHERKASY = 'cherkasy', 'Черкаси'
        CHERKASY_REGION = 'cherkasy_region', 'Черкаська область'
        SUMY = 'sumy', 'Суми'
        SUMY_REGION = 'sumy_region', 'Сумська область'
        ZHYTOMYR = 'zhytomyr', 'Житомир'
        ZHYTOMYR_REGION = 'zhytomyr_region', 'Житомирська область'
        CHERNIHIV = 'chernihiv', 'Чернігів'
        CHERNIHIV_REGION = 'chernihiv_region', 'Чернігівська область'
        RIVNE = 'rivne', 'Рівне'
        RIVNE_REGION = 'rivne_region', 'Рівненська область'
        LUTSK = 'lutsk', 'Луцьк'
        VOLYN_REGION = 'volyn_region', 'Волинська область'
        IVANO_FRANKIVSK = 'ivano_frankivsk', 'Івано-Франківськ'
        IVANO_FRANKIVSK_REGION = 'ivano_frankivsk_region', 'Івано-Франківська область'
        TERNOPIL = 'ternopil', 'Тернопіль'
        TERNOPIL_REGION = 'ternopil_region', 'Тернопільська область'
        UZHHOROD = 'uzhhorod', 'Ужгород'
        ZAKARPATTIA_REGION = 'zakarpattia_region', 'Закарпатська область'
        CHERNIVTSI = 'chernivtsi', 'Чернівці'
        CHERNIVTSI_REGION = 'chernivtsi_region', 'Чернівецька область'
        KHERSON = 'kherson', 'Херсон'
        KHERSON_REGION = 'kherson_region', 'Херсонська область'
        MYKOLAIV = 'mykolaiv', 'Миколаїв'
        MYKOLAIV_REGION = 'mykolaiv_region', 'Миколаївська область'
        KROPYVNYTSKYI = 'kropyvnytskyi', 'Кропивницький'
        KIROVOHRAD_REGION = 'kirovohrad_region', 'Кіровоградська область'
        KHMELNYTSKYI = 'khmelnytskyi', 'Хмельницький'
        KHMELNYTSKYI_REGION = 'khmelnytskyi_region', 'Хмельницька область'
        CRIMEA = 'crimea', 'Автономна Республіка Крим'
        DONETSK_REGION = 'donetsk_region', 'Донецька область'
        LUHANSK_REGION = 'luhansk_region', 'Луганська область'

    # characteristics
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)

    color = models.CharField(max_length=50)
    region = models.CharField(max_length=50, choices=Region)
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
    moderated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.car_model} {self.year}"


class CarImages(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="car_images")
    image = models.ImageField(upload_to='listing_images')
    is_main = models.BooleanField(default=False)
