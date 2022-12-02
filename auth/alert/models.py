from django.db import models
from uuid import UUID, uuid4
from organization.models import Organization

# Create your models here.


class RealTimeDatabase(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name="UUID",
    )
    # identifier = models.CharField(max_length=50)
    location_packet_type = models.CharField(max_length=25)
    message_body_length = models.CharField(max_length=25)
    imei = models.CharField(max_length=25)
    message_serial_number = models.IntegerField()
    alarm_series = models.IntegerField()
    terminal_status = models.BooleanField(default=False)
    ignition_status = models.BooleanField(default=False)
    latitude = models.IntegerField(blank=True, null=True)
    longitude = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    # direction = models.CharField(max_length=25, blank=True, null=True)
    # organization = models.ForeignKey(
    #     Organization, on_delete=models.CASCADE, blank=True, null=True
    # )
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.imei


class Alert(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name="UUID",
    )
    alert_video_url_china = models.TextField()
    alert_video_url_shoora = models.TextField(blank=True, null=True)
    device_imei = models.CharField(max_length=20)
    alert_time_epoch = models.PositiveBigIntegerField()
    alarm_type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
