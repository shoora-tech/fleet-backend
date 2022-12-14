from django.db import models
from uuid import uuid4

from organization.models import Organization, Branch

# Create your models here.


class DeviceType(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    MOVING = 'MOVING'
    STOPPED = 'STOPPED',
    IDLE = 'IDLE'
    UNKNOWN = 'UNKNOWN'
    STATUS_CHOICES = (
        (MOVING, 'moving'),
        (STOPPED, 'stopped'),
        (IDLE, 'idle'),
        (UNKNOWN, 'unknown')
    )
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    imei_number = models.CharField(max_length=20, unique=True)
    sim_number = models.PositiveBigIntegerField()
    activation_date = models.DateTimeField(
        blank=True, null=True
    )  # this will be automatically populated when
    # this device is linked to any vehicle
    ignition_status = models.BooleanField(default=False)
    speed = models.IntegerField(blank=True, null=True)
    # last_device_status = models.CharField(max_length=10,
    #               choices=STATUS_CHOICES,
    #               default=MOVING)
    last_device_status_timestamp = models.DateTimeField(blank=True, null=True)
    is_assigned_to_vehicle = models.BooleanField(default=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, blank=True, null=True, related_name="devices"
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, blank=True, null=True, related_name="devices"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.imei_number


# o1 -> 25
# 02 -> 25
# 03 -> 25
# 04 -> 25

# i1 --> [o1, o2]
# i2 --> [o3, o4]
