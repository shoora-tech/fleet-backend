from rest_framework import viewsets
from .serializers import DriverSerializer
from driver.models import Driver
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.viewsets import BaseViewSet
from rest_framework.response import Response
from rest_framework import status


class DriverViewSet(BaseViewSet):
    lookup_field = "uuid"
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
