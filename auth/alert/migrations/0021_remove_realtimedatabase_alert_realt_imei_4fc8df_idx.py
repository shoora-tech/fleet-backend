# Generated by Django 3.2.16 on 2023-01-08 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0020_realtimedatabase_alert_realt_imei_4fc8df_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='realtimedatabase',
            name='alert_realt_imei_4fc8df_idx',
        ),
    ]
