from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(RealTimeDatabase)
class RealtimeDBAdmin(admin.ModelAdmin):
    list_display = ("imei", "latitude", "longitude", "created_at")
