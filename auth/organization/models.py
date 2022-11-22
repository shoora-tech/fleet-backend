from uuid import uuid4
from django.db import models
from feature.models import Feature
from django.utils.translation import gettext as _

from auth.storage import get_image_upload_path

# Create your models here.
# id --> pk
class Organization(models.Model):
    contact_code_prefix = "+"
    uuid = models.UUIDField(
        unique=True, default=uuid4, editable=False, verbose_name=_("UUID")
    )
    name = models.CharField(max_length=50)
    address = models.TextField()
    registration_number = models.TextField()
    contact_code = models.IntegerField(max_length=4)
    contact_number = models.IntegerField(max_length=20)
    email = models.EmailField()
    features = models.ManyToManyField(Feature, related_name="organizations")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    chinese_server_username = models.CharField(max_length=20, blank=True, null=True)
    chinese_server_password = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
