from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.permissions import AccessControlPermission
from .serializers import VehicleSerializer
from vehicle.models import Vehicle
from auth.viewsets import BaseViewSet



class VehicleViewSet(BaseViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

