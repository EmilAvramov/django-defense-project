# Generated by Django 4.1.7 on 2023-07-27 13:44

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("account", "0002_customuser"),
    ]

    operations = [
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
                ("description", models.CharField(blank=True, max_length=100)),
            ],
            options={"verbose_name": "Role", "verbose_name_plural": "Roles",},
            bases=("auth.group",),
            managers=[("objects", django.contrib.auth.models.GroupManager()),],
        ),
        migrations.AddField(
            model_name="usermodel",
            name="roles",
            field=models.ManyToManyField(related_name="users", to="account.role"),
        ),
    ]