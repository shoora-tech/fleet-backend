# Generated by Django 3.2.16 on 2023-01-08 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0019_auto_20230102_1311'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='realtimedatabase',
            index=models.Index(fields=['imei'], name='alert_realt_imei_4fc8df_idx'),
        ),
    ]