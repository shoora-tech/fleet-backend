from django_filters import rest_framework as filters
from alert.models import RealTimeDatabase, Alert
from vehicle.models import Vehicle

class RealtimeDBFilter(filters.FilterSet):
    imei = filters.NumberFilter(field_name="imei")
    vehicle_id = filters.CharFilter(field_name="vehicle", method='filter_vehicle')

    class Meta:
        model = RealTimeDatabase
        fields = ['imei', 'vehicle_id']
    
    def filter_vehicle(self, queryset, name, value):
        try:
            vehicle = Vehicle.objects.get(uuid=value)
            gps = RealTimeDatabase.objects.filter(imei=str(vehicle.device.imei_number), is_corrupt=False).order_by("-created_at")[:1]
            return gps
        except Vehicle.DoesNotExist:
            return queryset.none()


class AlertFilter(filters.FilterSet):
    alerts_since = filters.IsoDateTimeFilter("created_at", lookup_expr="gte")
    alerts_until = filters.IsoDateTimeFilter("created_at", lookup_expr="lt")

    class Meta:
        model = Alert
        fields = ['alerts_since','alerts_until']