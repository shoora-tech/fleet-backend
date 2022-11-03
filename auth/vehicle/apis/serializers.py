from rest_framework import serializers
from vehicle.models import Vehicle
from vehicle.apis.serializers import VehicleSerializer
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    vehicle_type = serializers.ReadOnlyField
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Vehicle
        fields = (
            'id',
            'make',
            'model',
            'vin',
        )
