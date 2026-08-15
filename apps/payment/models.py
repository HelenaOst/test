from django.db import models

from apps.core.models import BaseModel


class CurrencyRate(BaseModel):
    """Курс валют за певну дату."""

    class Meta:
        db_table = 'currency_rate'
        ordering = ['-date']  # Сортування за спаданням дати

    date = models.DateField(unique=True)
    usd_to_uah = models.DecimalField(max_digits=10, decimal_places=4)
    eur_to_uah = models.DecimalField(max_digits=10, decimal_places=4)