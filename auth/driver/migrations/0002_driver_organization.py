# Generated by Django 3.2.16 on 2022-11-02 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0001_initial"),
        ("driver", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="organization.organization",
            ),
        ),
    ]
