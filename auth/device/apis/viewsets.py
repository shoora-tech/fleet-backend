from auth.viewsets import BaseViewSet
from rest_framework import viewsets, views, permissions
from .serializers import DeviceSerializer
from device.models import Device
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from organization.models import Organization
import requests


class DeviceViewSet(BaseViewSet):
    lookup_field = "uuid"
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceStatus(viewsets.ReadOnlyModelViewSet):
    queryset=Device.objects.all()
    serializer_class = DeviceSerializer

    def list(self, request, *args, **kwargs):
        print("cheching ststaus")
        if not request.user.is_authenticated:
            return Response({"detail": "Invalid access token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        device_status_param = {
            "jsession":"02d011cfea1840cea9f98a4b4e5d8589"
        }
        device_status_url = "https://dsm.shoora.com/StandardApiAction_getDeviceOlStatus.action"
        device_ids = request.GET.get("device_id", None)
        if device_ids:
            JWTA = JWTAuthentication()
            payload = request.auth.payload
            organization_id = payload["organization_id"]
            org = Organization.objects.get(uuid=organization_id)
            devices = Device.objects.filter(organization=org, imei_number__in=device_ids.split(','))
            if devices:
                imei = ','.join(dev.imei_number for dev in devices)
                device_status_param["devIdno"] = imei
                resp = requests.get(url=device_status_url, params=device_status_param)
                device_id_status_list = []
                if resp.status_code == 200:
                    data = resp.json()
                    onlines = data['onlines']
                    for item in onlines:
                        temp = {
                            "device_id": item['did'],
                            "status": 'online' if item['online'] == 1 else 'offline'
                        }
                        device_id_status_list.append(temp)
                data = {"result": device_id_status_list}
                return Response(data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)
        
