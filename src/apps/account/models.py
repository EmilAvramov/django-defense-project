from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django_defense_project.settings import AUTH_USER_MODEL
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator

from .managers import CustomUserManager

start_with_letter = RegexValidator(
    "^[A-Za-z]", "Your name must start with a letter!"
)
only_letters = RegexValidator(
    "^[A-Za-z]+$", "Fruit name should contain only letters!"
)
min_eight_letters = RegexValidator(
    "^.{8,}$", "Field should contain at least 8 symbols"
)
min_two_letters = RegexValidator(
    "^.{2,}$", "Field should contain at least 2 symbols"
)

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class Role(Group):
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class UserModel(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(
        verbose_name="Email",
        max_length=64,
        unique=True,
        db_index=True,
        validators=[start_with_letter, min_two_letters],
    )
    first_name = models.CharField(
        max_length=64, validators=[only_letters, min_two_letters]
    )
    last_name = models.CharField(
        max_length=64, validators=[only_letters, min_two_letters]
    )
    password = models.CharField(max_length=64, validators=[min_eight_letters])

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    roles = models.ManyToManyField(Role, related_name="users")

    class Meta:
        verbose_name = "Registered User"
        verbose_name_plural = "Registered Users"

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse(
            "user_detail", kwargs={"id": self.id, "email": self.email},
        )


class UserProfileModel(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(verbose_name="Age", blank=True, null=True)
    gender = models.CharField(
        verbose_name="Gender",
        max_length=6,
        choices=GENDER,
        blank=True,
        null=True,
    )
    image = models.URLField(
        verbose_name="Profile Picture", blank=True, null=True
    )
    digimons = models.ManyToManyField("main.Digimon", related_name="digimons")
    bookmarks = models.ManyToManyField(
        "main.Digimon", related_name="bookmarks"
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
