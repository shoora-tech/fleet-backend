# Generated by Django 3.2.16 on 2022-12-04 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0003_realtimedatabase_direction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="realtimedatabase",
            name="terminal_status",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
