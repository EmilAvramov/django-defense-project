from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(
        "Email", max_length=64, unique=True, db_index=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Registered User"
        verbose_name_plural = "Registered Users"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse(
            "user_detail", kwargs={"id": self.id, "email": self.email},
        )
