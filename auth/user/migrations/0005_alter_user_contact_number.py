# Generated by Django 3.2.16 on 2022-11-20 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_auto_20221112_1530"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="contact_number",
            field=models.BigIntegerField(),
        ),
    ]