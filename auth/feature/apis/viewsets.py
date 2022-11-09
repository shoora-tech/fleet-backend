from rest_framework import viewsets
from .serializers import FeatureSerializer
from feature.models import Feature


class FeatureViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
