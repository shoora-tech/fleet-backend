from uuid import uuid4
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Feature(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid4, editable=False, verbose_name=_("UUID")
    )
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
