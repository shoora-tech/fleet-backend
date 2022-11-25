from django.db import models
from uuid import UUID, uuid4
from organization.models import Organization
from driver.models import Driver

# Create your models here.


class RealTimeDatabase(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    identifier = models.CharField(max_length=50)
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
    direction = models.CharField(max_length=25, blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True
    )


severity_choices = (
    ('Low','Low'),
    ('Medium','Medium'),
    ('High', 'High')
)

class Alarm(models.Model):
    asset_id = models.CharField(max_length=10)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    event_type = models.CharField(max_length=50)
    date_time = models.DateTimeField(auto_now=True)
    severity = models.CharField(max_length=25, blank=True, null=True,choices=severity_choices)
    event_location = models.CharField(max_length=80, blank=True, null=True)
    actions = models.TextField(help_text="View/Comment", max_length=150, blank=True, null=True)
    
