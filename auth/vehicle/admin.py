from django.contrib import admin
from .models import *
from device.models import Device
from dal import autocomplete

# Register your models here.

admin.site.register(VehicleType)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)


from django import forms
class VehicleForm(forms.ModelForm):
    device = forms.ModelChoiceField(
                queryset=Device.objects.all(),
                widget=autocomplete.ModelSelect2(
                        url='vehicle_device_autocomplete',
                        forward=['organization']
                ),
            )
    class Meta:
        model = Vehicle
        fields = '__all__'

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vin", "make", "model", "vehicle_type",'last_status_update')
    autocomplete_fields = ["organization", "device"]
    list_per_page = 10
    search_fields = ['vin']
    list_filter = ['last_status_update']
    ordering = ['last_status_update']
    
    form = VehicleForm

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
    
    class Media:
        js = (
            'vehicle/js/chained_dd.js',
        )
