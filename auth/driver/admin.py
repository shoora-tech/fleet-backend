from django.contrib import admin
from .models import *
from vehicle.models import Vehicle
from dal import autocomplete


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


from django import forms
class DriverForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(
                queryset=Vehicle.objects.all(),
                widget=autocomplete.ModelSelect2(
                        url='driver_vehicle_autocomplete',
                        forward=['organization']
                ),
            )
    class Meta:
        model = Driver
        fields = '__all__'

# Register your models here.
class DriverAdmin(admin.ModelAdmin):
    # exclude=('driver_score',)
    list_display=('name','organization','vehicle')
    search_fields = ("name",)
    list_filter = (OrganizationTextFilter, VehicleTextFilter)
    form = DriverForm

admin.site.register(Driver,DriverAdmin)
admin.site.register(DriverHistory)
