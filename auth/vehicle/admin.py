from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(VehicleType)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("uuid", "make", "model", "vehicle_type")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization__in=request.user.installer_organizations.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "organization":
                kwargs["queryset"] = request.user.installer_organizations.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
