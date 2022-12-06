from rest_framework import serializers
from alert.models import RealTimeDatabase
from organization.apis.serializers import OrganizationSerializer


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
        )
