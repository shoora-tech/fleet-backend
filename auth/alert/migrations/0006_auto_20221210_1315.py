# Generated by Django 3.2.16 on 2022-12-10 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0005_rawalert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rawalert',
            old_name='alarm_type_1',
            new_name='alert_type_1',
        ),
        migrations.RenameField(
            model_name='rawalert',
            old_name='alarm_type_2',
            new_name='alert_type_2',
        ),
    ]
