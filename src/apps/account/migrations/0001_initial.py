# Generated by Django 4.1.7 on 2023-08-05 14:26

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True,
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Za-z]", "Must start with a letter!"
                            ),
                            django.core.validators.RegexValidator(
                                "^.{2,}$", "Must contain at least 2 symbols!"
                            ),
                        ],
                        verbose_name="Email",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Za-z]+$", "Must contain only letters!"
                            ),
                            django.core.validators.RegexValidator(
                                "^.{2,}$", "Must contain at least 2 symbols!"
                            ),
                        ],
                        verbose_name="First Name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[A-Za-z]+$", "Must contain only letters!"
                            ),
                            django.core.validators.RegexValidator(
                                "^.{2,}$", "Must contain at least 2 symbols!"
                            ),
                        ],
                        verbose_name="Last Name",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^.{8,}$", "Must contain at least 8 symbols!"
                            )
                        ],
                        verbose_name="Password",
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "verbose_name": "Registered User",
                "verbose_name_plural": "Registered Users",
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "group_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="auth.group",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=64)),
            ],
            options={"verbose_name": "Role", "verbose_name_plural": "Roles",},
            bases=("auth.group",),
            managers=[("objects", django.contrib.auth.models.GroupManager()),],
        ),
        migrations.CreateModel(
            name="UserProfileModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("age", models.IntegerField(blank=True, null=True, verbose_name="Age")),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female")],
                        max_length=6,
                        null=True,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "image",
                    models.URLField(
                        blank=True, null=True, verbose_name="Profile Picture"
                    ),
                ),
                (
                    "digimons",
                    models.ManyToManyField(related_name="digimons", to="main.digimon"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Profile",
                "verbose_name_plural": "User Profiles",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=64, unique=True, verbose_name="Email"),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=64, verbose_name="First Name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=64, verbose_name="Last Name"
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to.",
                        related_name="customuser_set",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="customuser_set",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="usermodel",
            name="roles",
            field=models.ManyToManyField(related_name="users", to="account.role"),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
