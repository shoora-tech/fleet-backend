from django_filters import rest_framework as filters
from alert.models import RealTimeDatabase

class RealtimeDBFilter(filters.FilterSet):
    imei = filters.NumberFilter(field_name="imei")

    class Meta:
        model = RealTimeDatabase
        fields = ['imei',]