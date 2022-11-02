from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")