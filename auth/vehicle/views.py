from device.models import Device
from vehicle.models import VehicleModel
from dal import autocomplete
# from .models import Item


class DeviceAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Device.objects.none()

        org = self.forwarded.get('organization', None)
        if org:
            qs = Device.objects.filter(organization=org, is_assigned_to_vehicle=False)
        else:
            qs = Device.objects.none()
        if self.q:
            qs = qs.filter(imei_number__istartswith=self.q)
        return qs


class VehicleModelAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return VehicleModel.objects.none()

        make = self.forwarded.get('make', None)
        if make:
            qs = VehicleModel.objects.filter(vehicle_make=make)
        else:
            qs = VehicleModel.objects.none()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
