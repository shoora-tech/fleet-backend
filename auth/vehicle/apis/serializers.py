from rest_framework import serializers
from vehicle.models import Vehicle, VehicleMake, VehicleModel, VehicleType, Geofence, VehicleGeofence, VehicleGroup
from alert.models import RealTimeDatabase
from organization.models import Organization, Branch

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
    organization = serializers.ReadOnlyField(source="organization.name")
    branch = serializers.ReadOnlyField(source="branch.name", allow_null=True)
    # branch_id = serializers.SlugRelatedField(source="branch", slug_field="uuid", queryset=Branch.objects.all())
    make = serializers.ReadOnlyField(source="make.name")
    model = serializers.ReadOnlyField(source="model.name")
    vehicle_type = serializers.ReadOnlyField(source="vehicle_type.name")
    device = serializers.ReadOnlyField(source="device.imei_number")
    driver = serializers.ReadOnlyField(source="driver.name")
    status = serializers.SerializerMethodField()
    last_device_status_timestamp = serializers.SerializerMethodField()
    

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
            "branch",
            "device",
            "driver",
            'status',
            'last_device_status_timestamp',
        )
    
    def get_status(self, obj):
        ignition_status = obj.device.ignition_status
        speed = obj.device.speed
        if ignition_status and speed > 0:
            return 'moving'
        elif ignition_status and speed == 0:
            return 'idle'
        elif not ignition_status:
            return 'stopped'
        return 'unknown'
    
    def get_last_device_status_timestamp(self, obj):
        return obj.device.last_device_status_timestamp


class VehicleGroupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    vehicle_ids = serializers.SlugRelatedField(source="vehicle", queryset=Vehicle.objects.all(), slug_field='uuid', many=True)
    # vehicle_group = serializers.SlugRelatedField(queryset=VehicleGroup.objects.all(), slug_field='uuid')
    # geofence = serializers.SlugRelatedField(queryset=Geofence.objects.all(), slug_field='uuid')
    organization_id = serializers.SlugRelatedField(source="organization", queryset=Organization.objects.all(), slug_field="uuid")
    branch_id = serializers.SlugRelatedField(source="branch", queryset=Branch.objects.all(), slug_field="uuid", allow_null=True, required=False)


    class Meta:
        model = VehicleGroup
        fields = ("id", "vehicle_ids", "organization_id", "branch_id", "name")


class GeofenceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    # vehicle = serializers.SlugRelatedField(queryset=Vehicle.objects.all(), slug_field='uuid', many=True)
    # vehicle_group = serializers.SlugRelatedField(queryset=VehicleGroup.objects.all(), slug_field='uuid')
    # geofence = serializers.SlugRelatedField(queryset=Geofence.objects.all(), slug_field='uuid')
    organization_id = serializers.SlugRelatedField(source="organization", queryset=Organization.objects.all(), slug_field="uuid")
    branch_id = serializers.SlugRelatedField(source="branch", queryset=Branch.objects.all(), slug_field="uuid", allow_null=True, required=False)


    class Meta:
        model = Geofence
        fields = ("id", "latitude", "longitude", "radius", "organization_id", "branch_id", "name")



class VehicleGeofenceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    vehicle_ids = serializers.SlugRelatedField(source="vehicle", queryset=Vehicle.objects.all(), slug_field='uuid', many=True)
    vehicle_group_ids = serializers.SlugRelatedField(source="vehicle_group", queryset=VehicleGroup.objects.all(), slug_field='uuid', many=True, required=False, allow_null=True)
    geofence_id = serializers.SlugRelatedField(source="geofence", queryset=Geofence.objects.all(), slug_field='uuid')
    organization_id = serializers.SlugRelatedField(source="organization", queryset=Organization.objects.all(), slug_field="uuid")
    branch_id = serializers.SlugRelatedField(source="branch", queryset=Branch.objects.all(), slug_field="uuid", allow_null=True, required=False)


    class Meta:
        model = VehicleGeofence
        fields = ("id", "vehicle_ids", "organization_id", "branch_id", "vehicle_group_ids", "geofence_id", "alert_type")



