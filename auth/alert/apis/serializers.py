from rest_framework import serializers
from alert.models import RealTimeDatabase
from alert.models import Alarm
from organization.apis.serializers import OrganizationSerializer


class AlertSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = RealTimeDatabase
        fields = (
            "id",
            "identifier",
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
            "organization",
        )


        model = Alarm
        fields = (
            "asset_id",
            "driver",
            "event_type",
            "date_time",
            "severity",
            "event_location",
            "actions",
        )
    

