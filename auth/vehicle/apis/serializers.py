from rest_framework import serializers
from vehicle.models import Vehicle, VehicleMake, VehicleModel, VehicleType, Geofence, VehicleGeofence, VehicleGroup
from alert.models import RealTimeDatabase
from organization.models import Organization, Branch
from alert.models import LatestGPS
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse
from driver.models import Driver



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
    class DriverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Driver
            fields = ("name",)
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
    driver = DriverSerializer(read_only=True, many=True)
    device = serializers.ReadOnlyField(source="device.imei_number")
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
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        drivers = data.pop("driver", None)
        if drivers:
            data["driver"] = drivers[0]['name']
        else:
            data['driver'] = None
        return data


class VehicleLatestGPSSerializer(serializers.ModelSerializer):
    class DriverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Driver
            fields = ("name",)
    # from driver.apis.serializers import DriverOnlySerializer
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="vehicles-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    organization = serializers.ReadOnlyField(source="organization.uuid")
    # branch = serializers.ReadOnlyField(source="branch.name", allow_null=True)
    # branch_id = serializers.SlugRelatedField(source="branch", slug_field="uuid", queryset=Branch.objects.all())
    make = serializers.ReadOnlyField(source="make.name")
    model = serializers.ReadOnlyField(source="model.name")
    vehicle_type = serializers.ReadOnlyField(source="vehicle_type.name")
    device = serializers.ReadOnlyField(source="device.imei_number")
    # driver = serializers.ReadOnlyField(source="driver.uuid", allow_null=True)
    # driver = serializers.SlugRelatedField(source="driver", slug_field="name", read_only=True)
    driver = DriverSerializer(read_only=True, many=True)
    last_device_status_timestamp = serializers.SerializerMethodField()
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
            # "branch",
            "device",
            "driver",
            'status',
            'last_device_status_timestamp',
            # 'current_location',
        )
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        drivers = data.pop("driver", None)
        if drivers:
            data["driver"] = drivers[0]['name']
        else:
            data['driver'] = None
        data['current_location'] = None
        return data
    
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
    
    # def get_driver(self, obj):
    #     driver = obj.driver.first()
    #     if driver:
    #         return driver.name
    #     return None
    
    # def get_current_location(self, obj):
    #     device = obj.device
    #     try:
    #         from alert.apis.serializers import LatestGpsSerializer
    #         lt = LatestGPS.objects.get(imei=device.imei_number)
    #         serializer = LatestGpsSerializer(lt, context=self.context)
    #         # serializer.is_valid(raise_exception=True)
    #         return serializer.data
    #     except LatestGPS.DoesNotExist:
    #         return None


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



