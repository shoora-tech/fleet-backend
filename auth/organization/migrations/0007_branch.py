# Generated by Django 3.2.16 on 2023-01-05 21:12

import auth.storage
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feature', '0001_initial'),
        ('organization', '0006_jsession'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('country_code', models.IntegerField()),
                ('contact_number', models.PositiveBigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=auth.storage.get_image_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('features', models.ManyToManyField(related_name='branches', to='feature.Feature')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
            ],
        ),
    ]