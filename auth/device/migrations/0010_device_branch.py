# Generated by Django 3.2.16 on 2023-01-06 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_branch'),
        ('device', '0009_auto_20221231_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='organization.branch'),
        ),
    ]
