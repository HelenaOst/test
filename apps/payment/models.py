from django.db import models

from apps.core.models import BaseModel


# Create your models here.
class CurrencyRate(BaseModel):
    date = models.DateField(unique=True)
    usd_to_uah = models.DecimalField(max_digits=10, decimal_places=4)
    eur_to_uah = models.DecimalField(max_digits=10, decimal_places=4)