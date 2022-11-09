from rest_framework import serializers
from organization.models import Organization
from driver.models import Driver
from vehicle.apis.serializers import VehicleSerializer
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse


class DriverSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    vehicle = VehicleSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = (
            "id",
            "name",
            "phone_number",
            "passport_number",
            "passport_validity",
            "driving_license_number",
            "driving_license_validity",
            "driver_score",
            "vehicle",
            "organization",
        )
