from django.contrib import admin

# Register your models here.
from trip.models import Trips

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

@admin.register(Trips)
class TripAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "duration", "distance", "created_at", "start_longitude", "end_longitude")
    list_filter = (OrganizationTextFilter, VehicleTextFilter)
