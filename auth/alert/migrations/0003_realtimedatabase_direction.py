# Generated by Django 3.2.16 on 2022-12-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0002_auto_20221202_1748"),
    ]

    operations = [
        migrations.AddField(
            model_name="realtimedatabase",
            name="direction",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]