from rest_framework import serializers
from organization.models import Organization
from driver.models import Driver
from vehicle.apis.serializers import VehicleSerializer
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse


class DriverSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="drivers-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    organization_id = serializers.SlugRelatedField(
        queryset=Organization.objects.all(), slug_field="uuid", source="organization"
    )
    vehicle = VehicleSerializer(read_only=True)
    # organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = (
            "id",
            "url",
            "name",
            "organization_id",
            "phone_number",
            "passport_number",
            "passport_validity",
            "driving_license_number",
            "driving_license_validity",
            "driver_score",
            "vehicle",
            # "organization",
        )


class DriverOnlySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="drivers-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    organization_id = serializers.SlugRelatedField(
        queryset=Organization.objects.all(), slug_field="uuid", source="organization"
    )
    # vehicle = VehicleSerializer(read_only=True)
    # organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = (
            "id",
            "url",
            "name",
            "organization_id",
            "phone_number",
            "passport_number",
            "passport_validity",
            "driving_license_number",
            "driving_license_validity",
            "driver_score",
            # "vehicle",
            # "organization",
        )
