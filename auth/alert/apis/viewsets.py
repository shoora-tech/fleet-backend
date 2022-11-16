from rest_framework import viewsets
from .serializers import AlertSerializer
from alert.models import RealTimeDatabase
from rest_framework_simplejwt.authentication import JWTAuthentication


class AlertViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = RealTimeDatabase.objects.all()
    serializer_class = AlertSerializer

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload["organization_id"]
        qs = self.queryset.filter(organization__uuid=organization_id)
        return qs
