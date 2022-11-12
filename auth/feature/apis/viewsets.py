from rest_framework import viewsets
from .serializers import FeatureSerializer
from feature.models import Feature
from rest_framework_simplejwt.authentication import JWTAuthentication


class FeatureViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        org = user.organization
        qs = org.features.all()
        return qs
