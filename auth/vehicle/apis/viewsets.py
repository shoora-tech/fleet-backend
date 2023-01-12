from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.permissions import GeoPermissions
from vehicle.apis.serializers import VehicleSerializer, VehicleListSerializer, VehicleGroupSerializer, GeofenceSerializer, VehicleGeofenceSerializer, VehicleLatestGPSSerializer
from vehicle.models import Vehicle, VehicleGroup, VehicleGeofence, Geofence
from auth.filters import VehicleFilter
from auth.viewsets import BaseViewSet
from organization.models import Organization, JSession
from rest_framework.response import Response
from rest_framework import status
from alert.models import LatestGPS
from alert.apis.serializers import LatestGpsSerializer
import requests



class VehicleViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all().prefetch_related('device', "organization", "vehicle_type", "model", "make", 'driver')
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
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        video = request.GET.get("video", None)
        # page = self.paginate_queryset(queryset)
        if not video:
            return super().list(request, *args, **kwargs)
            # if page is not None and video is None:
            #     serializer = self.get_serializer(page, many=True)
            #     return self.get_paginated_response(serializer.data)

            # serializer = self.get_serializer(queryset, many=True)

        serializer = self.serializer_class(queryset, context={"request": request}, many=True)
        data = serializer.data
        result = []
        # get video status
        
        if video:
            jsession = JSession.objects.first()
            jsession_id = jsession.jsesion
            device_status_param = {
                "jsession":jsession_id
            }
            device_status_url = "https://dsm.shoora.com/StandardApiAction_getDeviceOlStatus.action"
            imeis = list(queryset.values_list("device__imei_number", flat=True))
            imei = ','.join(imei for imei in imeis)
            device_status_param["devIdno"] = imei
            resp = requests.get(url=device_status_url, params=device_status_param)
            device_id_status_list = []
            if resp.status_code == 200:
                video_data = resp.json()
                video_data = video_data["onlines"]
                onlines = [d['vid'] for d in video_data]
                for d in data:
                    if video and d['vin'] in onlines:
                        d['video'] = 'online'
                        result.append(d)
                    elif not video and d['vin'] not in onlines:
                        d['video'] = 'offline'
                        result.append(d)
        resp = {}
        resp["count"] = queryset.count()
        resp["next"] = None
        resp["previous"] = None
        resp["results"] = result
        return Response(result, status=status.HTTP_200_OK)


class VehicleLatestGPSViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.prefetch_related('device', "organization", "vehicle_type", "model", "make", 'driver')
    serializer_class = VehicleLatestGPSSerializer
    filterset_class = VehicleFilter

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload["organization_id"]
        # organization_id = "b08eaad3-f9ee-44cc-a947-70bc2cd4cb89"
        org = Organization.objects.get(uuid=organization_id)
        qs = self.queryset.filter(organization=org).order_by("created_at")
        return qs
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, context={"request": request}, many=True)
        data = serializer.data
        # get location data for latestGps for these imeis
        imeis = []
        for d in data:
            imeis.append(d['device'])
        lts = LatestGPS.objects.filter(imei__in=imeis)
        lt_serializer = LatestGpsSerializer(lts, many=True)
        lt_data = lt_serializer.data
        for d in data:
            for lt in lt_data:
                if d['device'] == lt['imei']:
                    d['current_location'] = lt
                    lt_data.remove(lt)
                    break
        result = {}
        result["count"] = queryset.count()
        result["next"] = None
        result["previous"] = None
        result["results"] = data
        return Response(result, status=status.HTTP_200_OK)


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
