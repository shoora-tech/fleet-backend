# Generated by Django 4.1.3 on 2022-12-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0005_alter_device_last_device_status_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='activation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_device_status_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]