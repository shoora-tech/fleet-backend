from rest_framework import serializers
from organization.models import Organization
from feature.apis.serializers import FeatureSerializer
from feature.models import Feature
from rest_framework.reverse import reverse


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='uuid')
    features = FeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    roles_url = serializers.SerializerMethodField()
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
            'image',
            'roles_url',
            'vehicles_url',
            'features_url',
        )
    # def validate_contact_code(self):
    #     pass
    def create(self, validated_data):
        feature_ids = validated_data.pop("feature_ids", [])
        organization = super().create(validated_data)
        features = Feature.objects.filter(uuid__in=feature_ids)
        organization.features.add(*features)
        return organization
    

    def get_roles_url(self, org):
        return reverse('roles-list', request=self.context['request']) 

    def get_features_url(self, org):
        return reverse('features-list', request=self.context['request']) 
    
    def get_vehicles_url(self, org):
        return reverse('vehicles-list', request=self.context['request'])

