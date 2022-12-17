from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.


@admin.register(RealTimeDatabase)
class RealtimeDBAdmin(admin.ModelAdmin):
    list_display = ("imei", "latitude", "longitude", "created_at")

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "organization", "driver", "alarm_name", "created_at", "alert_video_url")
    list_per_page = 20

    def organization(self, obj):
        return obj.vehicle.organization.name

    def alert_video_url(self, obj):
        return format_html("<a href='{url}'>Watch Video</a>", url=obj.alert_video_url_shoora)
    
    def driver(self, obj):
        return obj.vehicle.driver.first()
