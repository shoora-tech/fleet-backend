from django.contrib import admin
from django.utils.html import format_html
from .models import *
from datetime import datetime

# Register your models here.


@admin.register(RealTimeDatabase)
class RealtimeDBAdmin(admin.ModelAdmin):
    list_display = ("imei", "latitude", "longitude", "created_at")

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "organization", "driver", "alarm_name", "alert_created_at", "alert_video_url")
    list_per_page = 20

    def alert_created_at(self, obj):
        alert_time_epoch = obj.alert_time_epoch
        if alert_time_epoch:
            try:
                alert_datetime = datetime.utcfromtimestamp(alert_time_epoch/1000)
                return alert_datetime
            except Exception as e:
                print("exceptrion ", e)
                return obj.created_at
        return obj.created_at

    def organization(self, obj):
        return obj.vehicle.organization.name

    def alert_video_url(self, obj):
        return format_html("<a href='{url}'>Watch Video</a>", url=obj.alert_video_url_shoora)
    
    def driver(self, obj):
        return obj.vehicle.driver.first()
