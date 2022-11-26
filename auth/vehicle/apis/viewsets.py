from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.permissions import AccessControlPermission
from .serializers import VehicleSerializer, VehicleMakeSerializer,VehicleModelSerializer,VehicleTypeSerializer
from vehicle.models import Vehicle, VehicleModel,VehicleMake,VehicleType
from auth.viewsets import BaseViewSet



class VehicleViewSet(BaseViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleMakeViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = VehicleMake.objects.all()
    serializer_class = VehicleMakeSerializer

class VehicleModelViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer 

class VehicleTypeViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer      
