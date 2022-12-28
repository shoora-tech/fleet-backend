from django.contrib import admin
from .models import *
from vehicle.models import Vehicle
from dal import autocomplete


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
    exclude=('driver_score',)
    list_display=('name','image','organization','vehicle')
    search_fields = ['name']
    list_per_page = 10
    list_filter = ['organization']
    form = DriverForm

admin.site.register(Driver,DriverAdmin)
admin.site.register(DriverHistory)
