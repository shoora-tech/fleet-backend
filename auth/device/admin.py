from django.contrib import admin
from .models import *
from alert.models import RealTimeDatabase

# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    list_display=('imei_number','sim_number','is_assigned_to_vehicle','organization')
    readonly_fields = ('is_assigned_to_vehicle', "get_activation_date","get_last_device_status_timestamp")
    search_fields = ("imei_number",)
    exclude = ("activation_date", "last_device_status_timestamp")

    def get_activation_date(self, obj):
        gps = RealTimeDatabase.objects.filter(imei=obj.imei_number).first()
        return gps.created_at
    
    def get_last_device_status_timestamp(self, obj):
        gps = RealTimeDatabase.objects.filter(imei=obj.imei_number).last()
        return gps.created_at
    
    get_last_device_status_timestamp.short_description = 'Last Device Status Time'
    get_activation_date.short_description = 'Device Activation Date'


admin.site.register(DeviceType)
admin.site.register(Device,DeviceAdmin)
