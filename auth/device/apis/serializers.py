from rest_framework import serializers
from device.models import Device
from organization.models import Branch
from rest_framework.reverse import reverse


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="devices-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    branch_id = serializers.SlugRelatedField(source="branch", slug_field="uuid", queryset=Branch.objects.all())
    device_type = serializers.StringRelatedField()

    class Meta:
        model = Device
        fields = (
            "id",
            "url",
            "device_type",
            "imei_number",
            "sim_number",
            "activation_date",
            "is_assigned_to_vehicle",
            "organization",
            "branch_id",
        )
