from rest_framework import serializers
from alert.models import RealTimeDatabase, Alert, LatestGPS
from vehicle.models import Vehicle
from driver.apis.serializers import DriverOnlySerializer


class RealTimeDatabaseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = RealTimeDatabase
        fields = (
            "id",
            # "location_packet_type",
            # "message_body_length",
            "imei",
            # "message_serial_number",
            # "alarm_series",
            # "terminal_status",
            "ignition_status",
            "latitude",
            "longitude",
            # "height",
            "speed",
            # "direction",
            "created_at",
        )


class LatestGpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestGPS
        fields = (
            "imei",
            "ignition_status",
            "latitude",
            "longitude",
            "speed",
            "created_at",
        )


class AlertSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    vehicle = serializers.SlugRelatedField(
        # queryset=Vehicle.objects.all(),
        slug_field="vin",
        read_only=True
    )
    # video_url = serializers.ReadOnlyField(source="alert_video_url_shoora",)
    alert_name = serializers.ReadOnlyField(source="alarm_name",)
    # driver = DriverSerializer(read_only=True, allow_null=True)
    driver = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = (
            "id",
            "video_url",
            "device_imei",
            "vehicle",
            "alert_name",
            "latitude",
            "longitude",
            "created_at",
            "driver",
        )
    
    def get_driver(self, alert):
        if alert.driver is not None:
            x = DriverOnlySerializer(alert.driver, context={'request': self.context['request']})
            return x.data
        driver = alert.vehicle.driver.first()
        if driver:
            x = DriverOnlySerializer(driver, context={'request': self.context['request']})
            return x.data
        return None
    
    def get_video_url(self, obj):
        # convert http to https
        request = self.context["request"]
        video_url = obj.alert_video_url_shoora
        if video_url:
            video_url = video_url.replace("http", "https")
        return video_url
            
            


