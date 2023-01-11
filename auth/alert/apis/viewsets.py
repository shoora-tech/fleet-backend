from rest_framework import viewsets
from .serializers import RealTimeDatabaseSerializer, AlertSerializer, LatestGpsSerializer
from alert.models import RealTimeDatabase, Alert, LatestGPS
from rest_framework_simplejwt.authentication import JWTAuthentication
from device.models import Device
from vehicle.models import Vehicle
from organization.models import Organization
from django.db.models import Max
from auth.filters import RealtimeDBFilter, AlertFilter, LatestGpsFilter

class RealtimeDatabaseViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = RealTimeDatabase.objects.all()
    serializer_class = RealTimeDatabaseSerializer
    filterset_class = RealtimeDBFilter

    def get_queryset(self):
        # payload = self.request.auth.payload
        # JWTA = JWTAuthentication()
        # user = JWTA.get_user(payload)
        # if user.is_superuser:
        #     return self.queryset
        # organization_id = payload["organization_id"]
        organization_id = "b08eaad3-f9ee-44cc-a947-70bc2cd4cb89"
        org = Organization.objects.get(uuid=organization_id)
        qs = self.queryset.filter(organization=org).distinct("imei")#.order_by('-created_at')#.values("uuid", "imei", "latitude", "longitude", "speed", "ignition_status", "created_at").distinct('imei')
        # qs = qs.order_by('imei', '-created_at').distinct('imei')
        return qs


class LatestGpsViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = LatestGPS.objects.all()
    serializer_class = LatestGpsSerializer
    filterset_class = LatestGpsFilter

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload["organization_id"]
        # organization_id = "b08eaad3-f9ee-44cc-a947-70bc2cd4cb89"
        org = Organization.objects.get(uuid=organization_id)
        qs = self.queryset.filter(organization=org)#.order_by('-created_at')#.values("uuid", "imei", "latitude", "longitude", "speed", "ignition_status", "created_at").distinct('imei')
        # qs = qs.order_by('imei', '-created_at').distinct('imei')
        return qs


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filterset_class = AlertFilter
    # filter_class = AlertFilter

    @property
    def filter_class(self):
        if self.action == "list":
            return AlertFilter

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload["organization_id"]
        # all imei number for devices in this organization
        vehicle_vins = list(Vehicle.objects.filter(organization__uuid=organization_id).values_list("id", flat=True))
        qs = self.queryset.filter(vehicle__id__in=vehicle_vins)
        # qs = qs.annotate(latest=Max('created_at'))
        qs = qs.order_by('-created_at')
        return qs
