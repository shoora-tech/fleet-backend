from rest_framework import serializers
from alert.models import RealTimeDatabase, Alert
from vehicle.models import Vehicle
from driver.apis.serializers import DriverSerializer


class RealTimeDatabaseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = RealTimeDatabase
        fields = (
            "id",
            "location_packet_type",
            "message_body_length",
            "imei",
            "message_serial_number",
            "alarm_series",
            "terminal_status",
            "ignition_status",
            "latitude",
            "longitude",
            "height",
            "speed",
            "direction",
            "created_at",
        )

class AlertSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    vehicle = serializers.SlugRelatedField(
        # queryset=Vehicle.objects.all(),
        slug_field="vin",
        read_only=True
    )
    video_url = serializers.ReadOnlyField(source="alert_video_url_shoora",)
    alert_name = serializers.ReadOnlyField(source="alarm_name",)
    # driver = DriverSerializer(read_only=True, allow_null=True)
    driver = serializers.SerializerMethodField()

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
            x = DriverSerializer(alert.driver)
            return x.data
        driver = alert.vehicle.driver.first()
        if driver:
            x = DriverSerializer(driver)
            return x.data
        return None


