from rest_framework import serializers
from organization.models import Organization
from feature.apis.serializers import FeatureSerializer
from feature.models import Feature


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    features = FeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'address',
            'contact_code',
            'contact_number',
            'email',
            'registration_number',
            'is_active',
            'features',
            'feature_ids',
            'image'
        )
    def create(self, validated_data):
        feature_ids = validated_data.pop("feature_ids", [])
        organization = super().create(validated_data)
        features = Feature.objects.filter(uuid__in=feature_ids)
        organization.features.add(*features)
        return organization
