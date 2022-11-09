from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.permissions import AccessControlPermission
from .serializers import VehicleSerializer
from vehicle.models import Vehicle



class VehicleViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    # permission_classes = [AccessControlPermission]



    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload['organization_id']
        qs = self.queryset.filter(organization__uuid=organization_id)
        return qs