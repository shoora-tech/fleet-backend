# Generated by Django 3.2.16 on 2022-12-22 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0015_alert_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='driver',
        ),
    ]
