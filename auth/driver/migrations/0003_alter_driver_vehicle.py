# Generated by Django 3.2.16 on 2022-12-14 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_vehicle_organization'),
        ('driver', '0002_driver_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='vehicle.vehicle'),
        ),
    ]
