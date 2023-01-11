# Generated by Django 3.2.16 on 2023-01-08 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_branch'),
        ('alert', '0021_remove_realtimedatabase_alert_realt_imei_4fc8df_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtimedatabase',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='live_data', to='organization.organization'),
        ),
    ]