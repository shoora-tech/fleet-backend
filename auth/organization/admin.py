from django.contrib import admin
from .models import *
from django.db.models import Count
from django.utils.html import format_html
from vehicle.models import Vehicle

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


    
