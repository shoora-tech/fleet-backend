# Generated by Django 3.2.16 on 2022-12-25 12:36

import auth.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0004_rename_drivehistory_driverhistory_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='driverhistory',
            options={'verbose_name_plural': 'Driver History'},
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_score',
            field=models.IntegerField(default=100, max_length=3),
        ),
        migrations.AlterField(
            model_name='driver',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=auth.storage.DriverImageStorageS3, upload_to=auth.storage.get_image_upload_path),
        ),
    ]