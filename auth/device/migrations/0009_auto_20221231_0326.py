# Generated by Django 3.2.16 on 2022-12-31 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0008_alter_device_imei_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='ignition_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='speed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]