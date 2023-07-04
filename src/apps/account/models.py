from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import CustomUserManager

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(
        verbose_name="Email", max_length=64, unique=True, db_index=True
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


class Profile(User):
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(
        verbose_name="Gender", max_length=6, choices=GENDER
    )
    digimons = models.ManyToManyField("main.Digimon", related_name="digimons")
    bookmarks = models.ManyToManyField(
        "main.Digimon", related_name="bookmarks"
    )
