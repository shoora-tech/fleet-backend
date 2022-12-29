# Generated by Django 3.2.16 on 2022-12-29 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20221228_1522'),
        ('device', '0006_alter_device_activation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='organization.organization'),
        ),
    ]
