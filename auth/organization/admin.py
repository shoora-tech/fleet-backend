from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "get_total_vehicles", "get_total_devices")
    search_fields = ("name",)

    def get_total_vehicles(self, obj):
        total_count = obj.vehicles.count()
        return total_count
    
    def get_total_devices(self, obj):
        total_count = obj.devices.count()
        return total_count
    
    get_total_vehicles.short_description = 'Total Vehicles'
    get_total_devices.short_description = 'Total Devices'
