from rest_framework import viewsets
from .serializers import DriverSerializer
from driver.models import Driver
from rest_framework_simplejwt.authentication import JWTAuthentication


class DriverViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload['organization_id']
        qs = self.queryset.filter(organization__uuid=organization_id)
        return qs
    
