from rest_framework import serializers
from feature.models import Feature


class FeatureSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="features-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )

    class Meta:
        model = Feature
        fields = (
            "id",
            "url",
            "name",
        )
