from auth.permissions import AccessControlPermission
from rest_framework import viewsets
from .serializers import DeviceSerializer
from device.models import Device


class DeviceViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [AccessControlPermission]
