# Generated by Django 3.2.16 on 2022-11-27 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0006_rename_alert_realtimedatabase"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="realtimedatabase",
            table="device_data_details",
        ),
    ]
