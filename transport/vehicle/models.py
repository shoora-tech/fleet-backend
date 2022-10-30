from django.db import models
from uuid import uuid4
# Create your models here.

# id, uuid, name
class Vehicle(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
