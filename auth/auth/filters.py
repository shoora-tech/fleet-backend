from django_filters import rest_framework as filters
from alert.models import RealTimeDatabase, Alert
from vehicle.models import Vehicle
from trip.models import Trips
from django.db.models import OuterRef, Subquery

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


class TripFilter(filters.FilterSet):
    vehicle_id = filters.UUIDFilter(field_name="vehicle__uuid",)
    class Meta:
        model = Trips
        fields = ("vehicle_id",)

class TripLocationFilter(filters.FilterSet):
    trip_id = filters.UUIDFilter(field_name="uuid",)
    class Meta:
        model = Trips
        fields = ("trip_id",)


class VehicleFilter(filters.FilterSet):
    vehicles_since = filters.IsoDateTimeFilter("created_at", lookup_expr="gte")
    vehicles_until = filters.IsoDateTimeFilter("created_at", lookup_expr="lt")
    # status = filters.CharFilter(method='filter_status')

    class Meta:
        model = Vehicle
        fields = ['vehicles_since','vehicles_until']
    
    # def filter_vehicle(self, queryset, name, value):
    #     if value == 'moving':
    #         # check for ignition_status=True and speed > 0
    #         rt = RealTimeDatabase.objects.filter()
    #         qs = queryset.filter(device__imei_number)
    #     try:
    #         vehicle = Vehicle.objects.get(uuid=value)
    #         gps = RealTimeDatabase.objects.filter(imei=str(vehicle.device.imei_number), is_corrupt=False).order_by("-created_at")[:1]
    #         return gps
    #     except Vehicle.DoesNotExist:
    #         return queryset.none()