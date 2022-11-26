from rest_framework import viewsets
from .serializers import AlertSerializer
from alert.models import RealTimeDatabase
from alert.models import Alarm
from auth.viewsets import BaseViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication


class AlertViewSet(BaseViewSet):
    lookup_field = "uuid"
    queryset = RealTimeDatabase.objects.all()
    queryset = Alarm.objects.all()
    serializer_class = AlertSerializer

    
