from rest_framework import serializers
from vehicle.models import Vehicle
# from vehicle.apis.serializers import VehicleTypeSerializer
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    # vehicle_type = VehicleTypeSerializer(read_only=True)
   
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Vehicle
        fields = (
            'id',
            'make',
            'model',
            'vin',
            'vehicle_type',
            'organization',
        )
