# Generated by Django 4.1.3 on 2022-12-12 16:58

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0003_rename_drivehistory_driverhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driving_license_validity',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date.today)]),
        ),
        migrations.AlterField(
            model_name='driver',
            name='passport_validity',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date.today)]),
        ),
    ]
