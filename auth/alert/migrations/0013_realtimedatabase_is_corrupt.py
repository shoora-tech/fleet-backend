# Generated by Django 3.2.16 on 2022-12-20 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0012_alter_realtimedatabase_message_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtimedatabase',
            name='is_corrupt',
            field=models.BooleanField(default=False),
        ),
    ]
