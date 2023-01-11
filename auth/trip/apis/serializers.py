from rest_framework import serializers
from organization.models import Organization
from driver.models import Driver
from vehicle.models import Vehicle
from vehicle.apis.serializers import VehicleSerializer
from organization.apis.serializers import OrganizationSerializer
from rest_framework.reverse import reverse
from trip.models import Trips
from driver.apis.serializers import DriverSerializer
from alert.models import RealTimeDatabase


class TripSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="trips-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    vehicle_id = serializers.SlugRelatedField(
        queryset=Vehicle.objects.all(), slug_field="uuid", source="vehicle",
    )
    driver = serializers.SerializerMethodField()
    gps_cordinates_url = serializers.SerializerMethodField()
    trip_started_at = serializers.SerializerMethodField()
    trip_ended_at = serializers.SerializerMethodField()
    # vehicle = VehicleSerializer(read_only=True)
    # organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Trips
        fields = (
            "id",
            "url",
            "start_latitude",
            "end_latitude",
            "start_longitude",
            "end_longitude",
            "duration",
            "distance",
            "total_incidents",
            # "driver_score",
            "vehicle_id",
            "driver",
            "gps_cordinates_url",
            # "organization",
            "created_at",
            "trip_started_at",
            "trip_ended_at",
        )
    
    def get_gps_cordinates_url(self, obj):
        return reverse("trips-path", kwargs={"uuid": obj.uuid}, request=self.context["request"])
    
    def get_driver(self, obj):
        driver = obj.driver
        if driver:
            return driver.name
        return None
    
    def get_trip_started_at(self, obj):
        gps_start = obj.gps_start
        if gps_start:
            rt = RealTimeDatabase.objects.get(id=gps_start)
            return rt.created_at
    
    def get_trip_ended_at(self, obj):
        gps_end = obj.gps_end
        if gps_end:
            rt = RealTimeDatabase.objects.get(id=gps_end)
            return rt.created_at


class TripLocationSerializer(serializers.ModelSerializer):
    gps_cordinates = serializers.SerializerMethodField()
    trip_started_at = serializers.SerializerMethodField()
    trip_ended_at = serializers.SerializerMethodField()

    class Meta:
        model = Trips
        fields = (
            "gps_cordinates",
            "trip_started_at",
            "trip_started_at",
        )
    
    def get_gps_cordinates(self, obj):
        gps_start = obj.gps_start
        gps_end = obj.gps_end
        location_points = []
        if gps_end and gps_start:
            location_points = list(RealTimeDatabase.objects.filter(
                id__gte=gps_start,
                id__lte=gps_end,
                imei=obj.vehicle.device.imei_number
                ).values_list("latitude", "longitude")
                )
        return location_points
    
    def get_trip_started_at(self, obj):
        gps_start = obj.gps_start
        if gps_start:
            rt = RealTimeDatabase.objects.get(id=gps_start)
            return rt.created_at
    
    def get_trip_ended_at(self, obj):
        gps_end = obj.gps_end
        if gps_end:
            rt = RealTimeDatabase.objects.get(id=gps_end)
            return rt.created_at


class TripStatsSerializer(serializers.Serializer):
    total_trips = serializers.IntegerField()
    total_distance = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    total_incidents = serializers.IntegerField()

