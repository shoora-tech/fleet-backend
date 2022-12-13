from django.contrib import admin
from .models import *

# Register your models here.

class Driveradmin(admin.ModelAdmin):
    list_display=('name','image','organization','vehicle')

admin.site.register(Driver,Driveradmin)
admin.site.register(DriverHistory)
