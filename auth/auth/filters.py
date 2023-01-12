from django_filters import rest_framework as filters
from alert.models import RealTimeDatabase, Alert, LatestGPS
from vehicle.models import Vehicle
from trip.models import Trips
from django.db.models import OuterRef, Subquery
from datetime import datetime, timedelta
from organization.models import Branch, JSession
from django.utils import timezone
import requests

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


class LatestGpsFilter(filters.FilterSet):
    imei = filters.NumberFilter(field_name="imei")
    vehicle_id = filters.CharFilter(field_name="vehicle", method='filter_vehicle')

    class Meta:
        model = LatestGPS
        fields = ['imei', 'vehicle_id']
    
    def filter_vehicle(self, queryset, name, value):
        try:
            vehicle = Vehicle.objects.get(uuid=value)
            try:
                gps = LatestGPS.objects.get(imei=str(vehicle.device.imei_number))
                return gps
            except LatestGPS.DoesNotExist:
                return queryset.none()
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
    status = filters.CharFilter(field_name='device', method='filter_status')
    # video_status = filters.CharFilter(field_name='device', method='filter_video_status')
    imei = filters.CharFilter(field_name="device__imei_number")

    class Meta:
        model = Vehicle
        fields = ['vehicles_since','vehicles_until', 'status', 'imei']
    
    # def filter_video_status(self, queryset, name, value):
    #     jsession = JSession.objects.first()
    #     jsession_id = jsession.jsesion
    #     device_status_param = {
    #         "jsession":jsession_id
    #     }
    #     device_status_url = "https://dsm.shoora.com/StandardApiAction_getDeviceOlStatus.action"
    #     imeis = list(queryset.values_list("device__imei_number", flat=True))
    #     imei = ','.join(imei for imei in imeis)
    #     device_status_param["devIdno"] = imei
    #     resp = requests.get(url=device_status_url, params=device_status_param)
    #     device_id_status_list = []
    #     if resp.status_code == 200:
    #         data = resp.json()
    #         data = data["onlines"]
    #         onlines = [d['vid'] for d in data]
    #         if value == "online":
    #             return queryset.filter(vin__in=onlines)
    #         else:
    #             return queryset.exclude(vin__in=onlines)
    
    def filter_status(self, queryset, name, value):
        time_threshold = timezone.now() - timedelta(hours=12)
        if value == 'moving':
            queryset = queryset.filter(device__ignition_status=True, device__speed__gt=0, device__last_device_status_timestamp__gte=time_threshold)
        elif value == 'idle':
            queryset = queryset.filter(device__ignition_status=True, device__speed=0, device__last_device_status_timestamp__gte=time_threshold)
        elif value == 'stopped':
            queryset = queryset.filter(device__ignition_status=False, device__last_device_status_timestamp__gte=time_threshold)
        elif value == 'offline':
            queryset = queryset.exclude(device__last_device_status_timestamp__gte=time_threshold)
        # elif value == 'online':
        #     time_threshold = timezone.now() - timedelta(minutes=10)
        #     print("threshold is ", time_threshold)
        #     queryset = queryset.filter(device__ignition_status=True, device__speed__gte=0)
        #     queryset = queryset.filter(device__last_device_status_timestamp__gte=time_threshold)
        return queryset


class BranchFilter(filters.FilterSet):
    organization_id = filters.UUIDFilter(field_name="organization",)
    class Meta:
        model = Branch
        fields = ("organization_id",)