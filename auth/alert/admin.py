from django.contrib import admin
from django.utils.html import format_html
from .models import *
from datetime import datetime
from django.contrib.admin import DateFieldListFilter

# Register your models here.

admin.site.register(RawAlert)




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


class VehicleTextFilter(admin.SimpleListFilter):
    title = 'Vehicle'
    parameter_name = 'vin'
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
            return queryset.filter(vehicle__vin__istartswith=value)


class GpsIdTextFilter(admin.SimpleListFilter):
    title = 'GPS ID'
    parameter_name = 'id'
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
            return queryset.filter(id__istartswith=value)


@admin.register(RealTimeDatabase)
class RealtimeDBAdmin(admin.ModelAdmin):
    list_display = ("id", "imei", "latitude", "longitude", "created_at")
    search_fields = ("imei",)
    list_filter = (GpsIdTextFilter, ('created_at', DateFieldListFilter),)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "organization", "driver", "alarm_name", "alert_created_at", "alert_video_url")
    list_filter = (VehicleTextFilter, OrganizationTextFilter, "alarm_name")
    list_per_page = 20

    def alert_created_at(self, obj):
        alert_time_epoch = obj.alert_time_epoch
        if alert_time_epoch:
            try:
                alert_datetime = datetime.utcfromtimestamp(alert_time_epoch/1000)
                return alert_datetime
            except Exception as e:
                print("exceptrion ", e)
                return obj.created_at
        return obj.created_at

    def organization(self, obj):
        return obj.vehicle.organization.name

    def alert_video_url(self, obj):
        return format_html("<a href='{url}'>Watch Video</a>", url=obj.alert_video_url_shoora)
    
    def driver(self, obj):
        return obj.vehicle.driver.first()
