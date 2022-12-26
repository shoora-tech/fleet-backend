from device.models import Device

from dal import autocomplete
# from .models import Item


class DeviceAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Device.objects.none()

        org = self.forwarded.get('organization', None)
        if org:
            qs = Device.objects.filter(organization=org, is_assigned_to_vehicle=False)
            print("qs is ", qs)
        else:
            qs = Device.objects.none()
        if self.q:
            qs = qs.filter(imei_number__istartswith=self.q)
        return qs
