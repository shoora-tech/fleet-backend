# Generated by Django 3.2.16 on 2023-01-08 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0023_realtimedatabase_alert_realt_organiz_d83d74_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='realtimedatabase',
            name='alert_realt_organiz_d83d74_idx',
        ),
    ]
