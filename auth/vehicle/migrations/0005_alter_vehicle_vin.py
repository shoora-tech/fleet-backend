# Generated by Django 3.2.16 on 2022-12-29 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0004_alter_vehicle_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vin',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
