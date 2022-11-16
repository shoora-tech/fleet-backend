# Generated by Django 3.2.16 on 2022-11-14 15:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0003_alter_alert_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'),
        ),
    ]