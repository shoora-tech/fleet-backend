# Generated by Django 3.2.16 on 2022-12-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_alter_trips_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='gps_end',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trips',
            name='gps_start',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]