from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    phone = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)


    def __str__(self):
        return self.username


class Account(models.Model):
    BASIC = "basic"
    PREMIUM = 'premium'
    TYPE_CHOICES = [
        (BASIC, "Basic"),
        (PREMIUM, "Premium")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=BASIC)
    expiry_at = models.DateTimeField(null=True, blank=True)

    @property
    @property
    def is_premium(self):
        if self.type != self.PREMIUM:
            return False
        if not self.expiry_at:
            return False
        return self.expiry_at > timezone.now()
