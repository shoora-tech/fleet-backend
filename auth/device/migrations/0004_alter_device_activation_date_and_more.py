# Generated by Django 4.1.3 on 2022-12-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_alter_device_sim_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='activation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_device_status_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
