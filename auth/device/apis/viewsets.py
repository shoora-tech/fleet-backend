from auth.viewsets import BaseViewSet
from rest_framework import viewsets
from .serializers import DeviceSerializer
from device.models import Device


class DeviceViewSet(BaseViewSet):
    lookup_field = "uuid"
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
