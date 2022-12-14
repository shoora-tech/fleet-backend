# Generated by Django 3.2.16 on 2022-11-01 15:13

import auth.storage
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("feature", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
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
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("address", models.TextField()),
                ("registration_number", models.TextField()),
                ("contact_code", models.IntegerField(max_length=4)),
                ("contact_number", models.IntegerField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("is_active", models.BooleanField(default=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=auth.storage.get_image_upload_path,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "features",
                    models.ManyToManyField(
                        related_name="organizations", to="feature.Feature"
                    ),
                ),
            ],
        ),
    ]
