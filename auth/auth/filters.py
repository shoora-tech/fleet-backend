from django_filters import rest_framework as filters
from alert.models import RealTimeDatabase, Alert

class RealtimeDBFilter(filters.FilterSet):
    imei = filters.NumberFilter(field_name="imei")

    class Meta:
        model = RealTimeDatabase
        fields = ['imei',]


class AlertFilter(filters.FilterSet):
    alert_time = filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Alert
        fields = ['alert_time',]