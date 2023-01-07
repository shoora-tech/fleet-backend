from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.permissions import GeoPermissions
from .serializers import VehicleSerializer, VehicleListSerializer, VehicleGroupSerializer, GeofenceSerializer, VehicleGeofenceSerializer
from vehicle.models import Vehicle, VehicleGroup, VehicleGeofence, Geofence
from auth.filters import VehicleFilter
from auth.viewsets import BaseViewSet



class VehicleViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_class = VehicleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return VehicleListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload["organization_id"]
        qs = self.queryset.filter(organization__uuid=organization_id).order_by("created_at")
        return qs


class VehicleGroupViewSet(BaseViewSet):
    queryset = VehicleGroup.objects.all()
    serializer_class = VehicleGroupSerializer


class VehicleGeofenceViewSet(BaseViewSet):
    queryset = VehicleGeofence.objects.all()
    serializer_class = VehicleGeofenceSerializer


class GeofenceViewSet(BaseViewSet):
    queryset = Geofence.objects.all()
    serializer_class = GeofenceSerializer
    permission_classes = [GeoPermissions]
