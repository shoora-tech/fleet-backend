from rest_framework import viewsets

from auth.permissions import AccessControlPermission
from .serializers import VehicleSerializer
from vehicle.models import Vehicle



class VehicleViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    # permission_classes = [AccessControlPermission]
