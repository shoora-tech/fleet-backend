from django.db import models
from uuid import uuid4
from driver.models import Driver
from vehicle.models import Vehicle

# Create your models here.


class Trips(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    start_location = models.CharField(max_length=50, blank=True, null=True)
    end_location = models.CharField(max_length=50, blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    total_incidents = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    driver = models.ForeignKey(Driver)
    vehicle = models.ForeignKey(Vehicle)
