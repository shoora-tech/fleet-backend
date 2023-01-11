from django.db import models
from uuid import uuid4
from organization.models import Organization, Branch
from device.models import Device
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

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
    IN = "IN_ALERT"
    OUT = "OUT_ALERT"
    BOTH = "BOTH"
    
    GEOFENCE_ALERT_CHOICES = (
        (IN, 'in'),
        (OUT, 'out'),
        (BOTH, 'both'),
    )
    uuid = models.UUIDField(verbose_name='UUID', default=uuid4, unique=True, editable=False)
    geofence = models.ForeignKey(Geofence, related_name='vehicle_geofences', on_delete=models.CASCADE)
    vehicle = models.ManyToManyField(Vehicle, related_name='vehicle_geofences', blank=True)
    vehicle_group = models.ManyToManyField(VehicleGroup, related_name='vehicle_geofences', blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="vehicle_geofences")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="vehicle_geofences", null=True, blank=True)
    alert_type = models.CharField(choices=GEOFENCE_ALERT_CHOICES, blank=True, null=True, verbose_name="Geofence Alert", max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Geofence)
def update_geofence_data(sender, instance, created, **kwargs):
    geo_obj = {
        "latitude": instance.latitude,
        "longitude": instance.longitude,
        "radius": instance.radius
    }
    print("updating ..")
    geos = str(instance.latitude)+","+str(instance.longitude)+","+str(instance.radius)
    from vehicle.tasks import update_geofence_redis
    update_geofence_redis.delay(str(instance.uuid), geos)


@receiver(post_delete, sender=Geofence)
def remove_geofence_from_redis(sender, instance, **kwargs):
    
    from vehicle.tasks import remove_geofence_redis
    remove_geofence_redis.delay(str(instance.uuid))


@receiver(post_delete, sender=Geofence)
def remove_geofence_from_associated_vehicles_in_redis(sender, instance, **kwargs):
    from vehicle.tasks import remove_geofence_from_vehicles_redis
    vehicle_geofence_ids = list(instance.vehicle_geofences.all().values("uuid"))
    remove_geofence_from_vehicles_redis.delay(vehicle_geofence_ids)


@receiver(post_delete, sender=VehicleGeofence)
def remove_geofence_from_associated_vehicles_in_redis(sender, instance, **kwargs):
    from vehicle.tasks import remove_geofence_from_vehicle_geofence_redis
    # vehicle_geofence_ids = list(instance.vehicle_geofences.all().values("uuid"))
    remove_geofence_from_vehicle_geofence_redis.delay(instance.uuid)


@receiver(post_save, sender=VehicleGeofence)
def update_vehicle_geofence(sender, instance, created, **kwargs):
    from vehicle.tasks import update_vehicle_geofence_redis
    update_vehicle_geofence_redis.delay(instance.uuid)