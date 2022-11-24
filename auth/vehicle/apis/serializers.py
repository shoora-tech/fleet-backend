from rest_framework import serializers
from vehicle.models import Vehicle, VehicleMake, VehicleModel, VehicleType

# from vehicle.apis.serializers import VehicleSerializer
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="vehicles-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    organization = OrganizationSerializer(read_only=True)
    make = serializers.SlugRelatedField(
        queryset=VehicleMake.objects.all(), slug_field="uuid"
    )
    model = serializers.SlugRelatedField(
        queryset=VehicleModel.objects.all(), slug_field="uuid"
    )
    vehicle_type = serializers.SlugRelatedField(
        queryset=VehicleType.objects.all(), slug_field="uuid"
    )

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "url",
            "make",
            "model",
            "vin",
            "vehicle_type",
            "organization",
        )
