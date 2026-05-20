from django.db import models

from apps.core.models import BaseModel
from apps.listing.models import Listing
from apps.users.models import User


# Create your models here.
class ListingView(BaseModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='views')
    viewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
