from django.db import models
from uuid import uuid4
from organization.models import Organization, Branch
import datetime
from django.core.validators import MinValueValidator
from auth.storage import get_image_upload_path, DriverImageStorageS3
from vehicle.models import Vehicle

# Create your models here.
class Driver(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True, storage=DriverImageStorageS3)
    phone_number = models.BigIntegerField()
    passport_number = models.CharField(max_length=8)
    passport_validity = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    driving_license_number = models.CharField(max_length=15)
    driving_license_validity = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    driver_score = models.IntegerField(default=100)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=True, null=True
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name="driver"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_driver_vehicle_history(self):
        # this will return the data containing all the vehicles along with their duration a driver was assigned to
        return self.drive_history.all()


class DriverHistory(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="drive_history"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="drive_history"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.driver.name} driving {self.vehicle.vin}"
    
    class Meta:
        verbose_name_plural = "Driver History"
