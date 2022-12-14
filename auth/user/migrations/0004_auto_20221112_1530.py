# Generated by Django 3.2.16 on 2022-11-12 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0001_initial"),
        ("user", "0003_role_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="installer_organizations",
            field=models.ManyToManyField(
                related_name="installers", to="organization.Organization"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="is_installer",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="role",
            name="display_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Display Name"
            ),
        ),
    ]
