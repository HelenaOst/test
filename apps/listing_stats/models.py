from django.db import models

from apps.core.models import BaseModel
from apps.listing.models import Listing
from apps.users.models import User


class ListingStats(BaseModel):
    """Статистика переглядів оголошень."""

    class Meta:
        db_table = 'listing_stats'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['listing']),
            models.Index(fields=['listing', 'created_at']),  # Для фільтрації за оголошенням + датою
        ]

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='views'
    )

    viewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
