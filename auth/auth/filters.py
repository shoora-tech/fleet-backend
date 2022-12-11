from django_filters import rest_framework as filters
from alert.models import RealTimeDatabase, Alert

class RealtimeDBFilter(filters.FilterSet):
    imei = filters.NumberFilter(field_name="imei")

    class Meta:
        model = RealTimeDatabase
        fields = ['imei',]


class AlertFilter(filters.FilterSet):
    alerts_since = filters.IsoDateTimeFilter("created_at", lookup_expr="gte")
    alerts_until = filters.IsoDateTimeFilter("created_at", lookup_expr="lt")

    class Meta:
        model = Alert
        fields = ['alerts_since','alerts_until']