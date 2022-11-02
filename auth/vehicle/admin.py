from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(VehicleType)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)
admin.site.register(Vehicle)