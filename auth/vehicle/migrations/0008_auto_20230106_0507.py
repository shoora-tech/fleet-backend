# Generated by Django 3.2.16 on 2023-01-06 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0007_geofence_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geofence',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='geofence',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
