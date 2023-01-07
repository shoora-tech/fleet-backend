from django.db import models
from uuid import uuid4
from organization.models import Organization, Branch
from device.models import Device
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class VehicleType(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VehicleMake(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=20)
    vehicle_make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE)
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    vin = models.CharField(max_length=25, unique=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    last_status_update = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True, related_name="vehicles"
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=True, null=True, related_name="vehicles"
    )
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vin}"

@receiver(post_save, sender=Vehicle)
def update_device_status(sender, instance, created, **kwargs):
    device = instance.device
    if device:
        device.is_assigned_to_vehicle = True
        device.save()


class VehicleGroup(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid4, unique=True, editable=False)
    vehicle = models.ManyToManyField(Vehicle, related_name="vehicle_groups")
    name = models.CharField(verbose_name="Group Name", max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="vehicle_groups")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="vehicle_groups", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Geofence(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name="UUID",
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.PositiveIntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="geofences")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="geofences", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VehicleGeofence(models.Model):
    uuid = models.UUIDField(verbose_name='UUID', default=uuid4, unique=True, editable=False)
    geofence = models.ForeignKey(Geofence, related_name='vehicle_geofences', on_delete=models.CASCADE)
    vehicle = models.ManyToManyField(Vehicle, related_name='vehicle_geofences', blank=True)
    vehicle_group = models.ManyToManyField(VehicleGroup, related_name='vehicle_geofences', blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="vehicle_geofences")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="vehicle_geofences", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
