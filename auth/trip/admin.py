from django.contrib import admin

# Register your models here.
from trip.models import Trips

@admin.register(Trips)
class TripAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "duration", "distance", "created_at")
