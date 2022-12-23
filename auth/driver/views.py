from django.shortcuts import render
from dal import autocomplete
from vehicle.models import Vehicle


class DriverAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Vehicle.objects.none()

        org = self.forwarded.get('organization', None)
        if org:
            qs = Vehicle.objects.filter(organization=org)
        else:
            qs = Vehicle.objects.none()
        if self.q:
            qs = qs.filter(vin__istartswith=self.q)
        return qs
