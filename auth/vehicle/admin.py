from django.contrib import admin
from .models import *
from device.models import Device
from dal import autocomplete
from driver.models import Driver
from django.db.models import Count, Q

# Register your models here.

admin.site.register(VehicleType)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)


class OrganizationTextFilter(admin.SimpleListFilter):
    title = 'Organization'
    parameter_name = 'name'
    template = 'admin_input_filter.html'

    def lookups(self, request, model_admin):
        return ((None, None),)

    def choices(self, changelist):
        query_params = changelist.get_filters_params()
        query_params.pop(self.parameter_name, None)
        all_choice = next(super().choices(changelist))
        all_choice['query_params'] = query_params
        yield all_choice

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(organization__name__istartswith=value)


class DeviceTextFilter(admin.SimpleListFilter):
    title = 'Device'
    parameter_name = 'imei_number'
    template = 'admin_input_filter.html'

    def lookups(self, request, model_admin):
        return ((None, None),)

    def choices(self, changelist):
        query_params = changelist.get_filters_params()
        query_params.pop(self.parameter_name, None)
        all_choice = next(super().choices(changelist))
        all_choice['query_params'] = query_params
        yield all_choice

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(device__imei_number__istartswith=value)


from django import forms
class VehicleForm(forms.ModelForm):
    device = forms.ModelChoiceField(
                queryset=Device.objects.all(),
                widget=autocomplete.ModelSelect2(
                        url='vehicle_device_autocomplete',
                        forward=['organization']
                ),
            )
    model = forms.ModelChoiceField(
                queryset=VehicleModel.objects.all(),
                widget=autocomplete.ModelSelect2(
                        url='vehicle_model_autocomplete',
                        forward=['make']
                ),
            )
    class Meta:
        model = Vehicle
        fields = '__all__'


class DriverInline(admin.TabularInline):
    fields = ["name", "phone_number", "driver_score"]
    readonly_fields = ["name", "phone_number", "driver_score"]
    extra = 0
    model = Driver


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vin", "make", "model", "vehicle_type",'created_at', "get_last_device_timestamp", "get_organization_name")
    autocomplete_fields = ["organization", "device"]
    list_per_page = 20
    search_fields = ("vin",)
    list_filter = (OrganizationTextFilter, DeviceTextFilter)
    inlines = (DriverInline,)
    form = VehicleForm
    search_help_text = 'Please input community id'

    def render_change_form(self, request, context, *args, **kwargs):
        form_instance = context['adminform'].form
        form_instance.fields['vin'].widget.attrs['placeholder'] = 'Your street'
        return super().render_change_form(request, context, *args, **kwargs)

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
    
    def get_organization_name(self, obj):
        return obj.organization.name
    
    def get_last_device_timestamp(self, obj):
        return obj.device.last_device_status_timestamp
    
    get_organization_name.short_description = 'Organization'
    get_last_device_timestamp.short_description = "Last Device Time"


@admin.register(VehicleGroup)
class VehicleGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "branch", "get_total_vehicles")

    def get_total_vehicles(self, obj):
        return obj.vehicle.count()


@admin.register(VehicleGeofence)
class VehicleGeofenceAdmin(admin.ModelAdmin):
    list_display = ("organization", "branch", "get_total_vehicles")

    def get_total_vehicles(self, obj):
        vehicles = list(obj.vehicle.values_list("id", flat=True))
        vehicle_count = len(vehicles)
        vehicles_in_group = obj.vehicle_group.annotate(vehicle_count=Count('vehicle', filter=~Q(vehicle__id__in=vehicles)))
        for vehicle in vehicles_in_group:
            vehicle_count += vehicle.vehicle_count
        return vehicle_count
    
    get_total_vehicles.short_description = "Total Vehicles"
@admin.register(Geofence)
class GeofeneAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "branch", )
