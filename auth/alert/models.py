from django.db import models
from uuid import UUID, uuid4
from organization.models import Organization
from vehicle.models import Vehicle

# Create your models here.


class RealTimeDatabase(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name="UUID",
    )
    location_packet_type = models.CharField(max_length=25)
    message_body_length = models.CharField(max_length=25)
    imei = models.CharField(max_length=25)
    message_serial_number = models.CharField(max_length=20)
    alarm_series = models.IntegerField()
    terminal_status = models.CharField(max_length=10, blank=True, null=True)
    ignition_status = models.BooleanField(default=False)
    latitude = models.CharField(blank=True, null=True, max_length=20)
    longitude = models.CharField(blank=True, null=True, max_length=20)
    height = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    direction = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

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
    alarm_name = models.CharField(
        verbose_name="Alarm Name",
        max_length=100,
        blank=True,
        null=True,
    )
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    guid = models.CharField(max_length=100, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RawAlert(models.Model):
    device_id_no = models.CharField(max_length=50)
    alert_latitude = models.CharField(max_length=20, blank=True, null=True)
    alert_longitude = models.CharField(max_length=20, blank=True, null=True)
    alert_description = models.CharField(max_length=100, blank=True, null=True)
    alert_guid = models.CharField(max_length=100, blank=True, null=True)
    hd = models.CharField(max_length=10)
    info = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    p1 = models.CharField(max_length=10)
    p2 = models.CharField(max_length=10)
    p3 = models.CharField(max_length=10)
    p4 = models.CharField(max_length=10)
    rve = models.CharField(max_length=10)
    alert_type_1 = models.CharField(max_length=10)
    src_tm = models.CharField(max_length=50)
    alert_type_2 = models.CharField(max_length=10)
    time = models.CharField(max_length=50)
    alert_type_3 = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class LatStoredValue(models.Model):
#     rtd_id = models.IntegerField(blank=True, null=True)
