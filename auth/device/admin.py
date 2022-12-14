from django.contrib import admin
from .models import *
from alert.models import RealTimeDatabase

# Register your models here.

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


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display=('imei_number','sim_number','is_assigned_to_vehicle','organization', 'last_device_status_timestamp')
    readonly_fields = ('is_assigned_to_vehicle', "get_activation_date",)
    search_fields = ("imei_number",)
    exclude = ("activation_date",)
    list_filter = (OrganizationTextFilter, "is_assigned_to_vehicle")
    list_per_page = 20

    def get_activation_date(self, obj):
        gps = RealTimeDatabase.objects.filter(imei=obj.imei_number)[:1]
        if gps:
            return gps.created_at
        return None
    
    # def get_last_device_status_timestamp(self, obj):
    #     gps = RealTimeDatabase.objects.filter(imei=obj.imei_number).last()
    #     return gps.created_at
    
    # get_last_device_status_timestamp.short_description = 'Last Device Status Time'
    get_activation_date.short_description = 'Device Activation Date'


admin.site.register(DeviceType)
# admin.site.register(Device,DeviceAdmin)
# admin.site.register(Device)
