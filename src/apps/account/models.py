from django.db import models
from django.urls import reverse


class User(models.Model):
    email = models.EmailField(
        "Email", max_length=64, unique=True, db_index=True
    )
    username = models.CharField(
        "Username", max_length=64, unique=True, db_index=True
    )
    password = models.CharField("Password", max_length=64)
    first_name = models.CharField("First Name", max_length=64)
    last_name = models.CharField("Last Name", max_length=64)

    class Meta:
        verbose_name = "Registered User"
        verbose_name_plural = "Registered Users"

    def __str__(self):
        return f"${self.username}, ${self.email}, ${self.first_name} ${self.last_name}"

    def get_absolute_url(self):
        return reverse(
            "user_detail",
            kwargs={
                "id": self.id,
                "email": self.email,
                "username": self.username,
            },
        )
