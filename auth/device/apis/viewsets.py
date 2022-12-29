from auth.viewsets import BaseViewSet
from rest_framework import viewsets, views, permissions
from .serializers import DeviceSerializer
from device.models import Device
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from organization.models import Organization, JSession
import requests
from django.conf import settings

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
        jsession_id = None
        jsession = JSession.objects.first()
        if not jsession:
            login_url = settings.JSESSION_URL
            resp = requests.get(url=login_url)
            if resp.status_code == 200:
                # save the jsession id
                data = resp.json()
                jsession_id = data['jsession']
                obj, created = JSession.objects.update_or_create(jsesion=data['jsession'])
        else:
            jsession_id = jsession.jsesion
        device_status_param = {
            "jsession":jsession_id
        }
        device_status_url = "https://dsm.shoora.com/StandardApiAction_getDeviceOlStatus.action"
        device_ids = request.GET.get("device_id", None)
        if device_ids and jsession_id:
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
        
