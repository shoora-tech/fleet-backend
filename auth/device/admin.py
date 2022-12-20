from django.contrib import admin
from .models import *

# Register your models here.

class Deviceadmin(admin.ModelAdmin):
    list_display=('imei_number','sim_number','is_assigned_to_vehicle','organization')

admin.site.register(DeviceType)
admin.site.register(Device,Deviceadmin)
