from rest_framework import viewsets
from .serializers import RealTimeDatabaseSerializer, AlertSerializer
from alert.models import RealTimeDatabase, Alert
from rest_framework_simplejwt.authentication import JWTAuthentication
from device.models import Device
from vehicle.models import Vehicle
from django.db.models import Max
from auth.filters import RealtimeDBFilter, AlertFilter

class RealtimeDatabaseViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = RealTimeDatabase.objects.all()
    serializer_class = RealTimeDatabaseSerializer
    filterset_class = RealtimeDBFilter

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return self.queryset
        organization_id = payload["organization_id"]
        # all imei number for devices in this organization
        device_imeis = list(Device.objects.filter(organization__uuid=organization_id, is_assigned_to_vehicle=True).values_list("imei_number", flat=True))
        qs = self.queryset.filter(imei__in=device_imeis)
        # qs = qs.annotate(latest=Max('created_at'))
        qs = qs.order_by('imei', '-created_at').distinct('imei')
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
            print("filtering ..")
            return AlertFilter

    def get_queryset(self):
        print("getting qs")
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
        qs = qs.order_by('guid', 'created_at').distinct('guid')
        return qs
