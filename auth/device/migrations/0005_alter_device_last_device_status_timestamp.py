# Generated by Django 4.1.3 on 2022-12-20 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_alter_device_activation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_device_status_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]