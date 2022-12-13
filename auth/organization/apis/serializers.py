from rest_framework import serializers
from organization.models import Organization
from feature.apis.serializers import FeatureSerializer
from feature.models import Feature
from rest_framework.reverse import reverse


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="organizations-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    features = FeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )

    class Meta:
        model = Organization
        fields = (
            "id",
            "url",
            "name",
            "address",
            "country_code",
            "contact_number",
            "email",
            "is_active",
            "features",
            "feature_ids",
            "image",
        )

    # def validate_contact_code(self):
    #     pass
    def create(self, validated_data):
        feature_ids = validated_data.pop("feature_ids", [])
        organization = super().create(validated_data)
        features = Feature.objects.filter(uuid__in=feature_ids)
        organization.features.add(*features)
        return organization
