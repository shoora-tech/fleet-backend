from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name",)
    list_filter = ['address']
    list_per_page = 10
