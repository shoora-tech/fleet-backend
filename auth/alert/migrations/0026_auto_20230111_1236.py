# Generated by Django 3.2.16 on 2023-01-11 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_branch'),
        ('alert', '0025_realtimedatabase_alert_realt_organiz_d83d74_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestGPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_packet_type', models.CharField(max_length=25)),
                ('message_body_length', models.CharField(max_length=25)),
                ('imei', models.CharField(max_length=25)),
                ('message_serial_number', models.CharField(max_length=20)),
                ('alarm_series', models.IntegerField()),
                ('terminal_status', models.CharField(blank=True, max_length=10, null=True)),
                ('ignition_status', models.BooleanField(default=False)),
                ('latitude', models.CharField(blank=True, max_length=20, null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('speed', models.IntegerField(blank=True, null=True)),
                ('direction', models.IntegerField(blank=True, null=True)),
                ('is_corrupt', models.BooleanField(default=False)),
                ('raw_hex_data', models.TextField(blank=True, null=True)),
                ('device_time', models.CharField(blank=True, max_length=12, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_gps', to='organization.organization')),
            ],
        ),
        migrations.AddIndex(
            model_name='latestgps',
            index=models.Index(fields=['organization'], name='alert_lates_organiz_111ad7_idx'),
        ),
    ]
