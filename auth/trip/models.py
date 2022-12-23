from django.db import models
from uuid import uuid4
from driver.models import Driver
from vehicle.models import Vehicle

# Create your models here.


class Trips(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    # start_location = models.CharField(max_length=50, blank=True, null=True)
    end_location = models.CharField(max_length=50, blank=True, null=True)
    start_latitude = models.CharField(blank=True, null=True, max_length=20)
    end_latitude = models.CharField(blank=True, null=True, max_length=20)
    start_longitude = models.CharField(blank=True, null=True, max_length=20)
    end_longitude = models.CharField(blank=True, null=True, max_length=20)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    total_incidents = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Trips"
