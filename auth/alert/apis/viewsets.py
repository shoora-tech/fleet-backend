from rest_framework import viewsets
from .serializers import RealTimeDatabaseSerializer
from alert.models import RealTimeDatabase
from rest_framework_simplejwt.authentication import JWTAuthentication
from device.models import Device
from django.db.models import Max
from auth.filters import RealtimeDBFilter

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
