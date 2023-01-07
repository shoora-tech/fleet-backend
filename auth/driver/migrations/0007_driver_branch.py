# Generated by Django 3.2.16 on 2023-01-06 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_branch'),
        ('driver', '0006_alter_driver_driver_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.branch'),
        ),
    ]