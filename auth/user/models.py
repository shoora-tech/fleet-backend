from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from uuid import UUID, uuid4
from django.utils.translation import gettext as _

from organization.models import Organization
from feature.models import Feature
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("users must have an Email")

        
        user = self.model(
            email=self.normalize_email(email),
            name=email.split('@')[0],
            contact_code=91,
            contact_number=1234567890,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    contact_code_prefix = "+"
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_code = models.IntegerField()
    contact_number = models.IntegerField()
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, blank=True, null=True, verbose_name=_("Organization"), related_name="users" ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.ManyToManyField("role", related_name="users", blank=True, null=True)

    USERNAME_FIELD = "email"
    objects = MyAccountManager()

    def __str__(self) -> str:
        return self.email or self.phone_number
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin


class Role(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class AccessControl(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    feature = models.ForeignKey(Feature, verbose_name=_("feature"), on_delete=models.CASCADE)
    role = models.ForeignKey(Role, verbose_name=_("role"), on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
