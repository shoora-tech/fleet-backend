from rest_framework import serializers
from vehicle.models import Vehicle
from rest_framework.reverse import reverse


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    class Meta:
        model = Vehicle
        fields = (
            'id',
            'vin',
        )
