from rest_framework import serializers
from vehicle.models import Vehicle, VehicleMake, VehicleModel, VehicleType
from alert.models import RealTimeDatabase

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
    device = serializers.SlugRelatedField(
        queryset=VehicleType.objects.all(), slug_field="imei_number"
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
            "device",
        )


class VehicleListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="vehicles-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    # organization = OrganizationSerializer(read_only=True)
    # organization = serializers.SlugRelatedField(
    #     queryset=Organization.objects.all(), slug_field="uuid"
    # )
    organization = serializers.ReadOnlyField(source="organization.name")
    make = serializers.ReadOnlyField(source="make.name")
    model = serializers.ReadOnlyField(source="model.name")
    vehicle_type = serializers.ReadOnlyField(source="vehicle_type.name")
    device = serializers.ReadOnlyField(source="device.imei_number")
    status = serializers.SerializerMethodField()
    

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
            "device",
            'status',
        )
    
    def get_status(self, obj):
        rt = RealTimeDatabase.objects.filter(imei=obj.device.imei_number)
        if rt:
            rt = rt.last()
            ignition_status = rt.ignition_status
            if ignition_status and rt.speed > 0:
                return 'moving'
            elif ignition_status and rt.speed == 0:
                return 'idle'
            elif not ignition_status:
                return 'stopped'
            return 'unknown'
        return 'unknown'

