from django.db import models


class Brand(models.Model):
    """Бренд/марка автомобіля."""

    class Meta:
        ordering = ['id']

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Модель автомобіля, прив'язана до бренду."""

    class Meta:
        db_table = 'car_model'
        ordering = ['id']
        constraints = [
            # Унікальність пари (бренд, модель) - запобігає дубляжу
            models.UniqueConstraint(fields=['brand', 'name'], name='unique_brand_car_model'),
        ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} {self.name}"