# Generated by Django 3.2.16 on 2022-12-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_rename_contact_code_organization_country_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='contact_number',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country_code',
            field=models.IntegerField(),
        ),
    ]
