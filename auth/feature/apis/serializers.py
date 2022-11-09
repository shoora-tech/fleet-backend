from rest_framework import serializers
from feature.models import Feature


class FeatureSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = Feature
        fields = (
            "id",
            "name",
        )
