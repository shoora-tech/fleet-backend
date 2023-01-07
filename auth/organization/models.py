from uuid import uuid4
from django.db import models
from feature.models import Feature
from django.utils.translation import gettext as _

from auth.storage import get_image_upload_path
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# id --> pk
class Organization(models.Model):
    contact_code_prefix = "+"
    uuid = models.UUIDField(
        unique=True, default=uuid4, editable=False, verbose_name=_("UUID")
    )
    name = models.CharField(max_length=50)
    address = models.TextField()
    country_code = models.IntegerField()
    contact_number = models.PositiveBigIntegerField()
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


class JSession(models.Model):
    jsesion = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Branch(models.Model):
    uuid = models.UUIDField(verbose_name='UUID', unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=50)
    address = models.TextField()
    country_code = models.IntegerField()
    contact_number = models.PositiveBigIntegerField()
    email = models.EmailField()
    features = models.ManyToManyField(Feature, related_name="branches")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



@receiver(post_save, sender=Organization)
def create_branch(sender, instance, created, **kwargs):
    if created:
        print("created")
        Branch.objects.create(
            name=instance.name,
            address=instance.address,
            country_code=instance.country_code,
            contact_number=instance.contact_number,
            email=instance.email,
            image=instance.image,
            organization=instance
        )
