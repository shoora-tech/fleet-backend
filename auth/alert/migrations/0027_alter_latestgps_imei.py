# Generated by Django 3.2.16 on 2023-01-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0026_auto_20230111_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestgps',
            name='imei',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
