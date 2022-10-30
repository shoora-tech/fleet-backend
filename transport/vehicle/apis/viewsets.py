from rest_framework import viewsets

from transport.permissions import VehiclePermission
from .serializers import VehicleSerializer
from vehicle.models import Vehicle



class VehicleViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [VehiclePermission]
