# Generated by Django 4.1.3 on 2022-12-20 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_rename_contact_code_user_country_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='country_code',
            new_name='contact_code',
        ),
    ]
