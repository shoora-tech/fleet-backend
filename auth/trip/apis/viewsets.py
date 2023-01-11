from rest_framework import viewsets
from .serializers import DriverSerializer
from driver.models import Driver
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth.viewsets import BaseViewSet
from rest_framework.response import Response
from rest_framework import status
from trip.models import Trips
from trip.apis.serializers import TripSerializer, TripLocationSerializer, TripStatsSerializer
from auth.filters import TripFilter, TripLocationFilter
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count


class TripViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
    filterset_class = TripFilter

    @property
    def filter_class(self):
        if self.action == "list":
            print("filtering ..")
            return TripFilter
    
    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        qs = self.queryset
        if self.action == "list":
            if user.is_superuser:
                return self.queryset.order_by("-created_at")
            organization_id = payload["organization_id"]
            qs = self.queryset.filter(vehicle__organization__uuid=organization_id)
            return qs.order_by("-created_at")
        return qs
    
    @action(detail=True, methods=['get'], url_path='path')
    def path(self, request, **kwargs):
        trip = self.get_object()
        serializer = TripLocationSerializer(trip)
        return Response(serializer.data)



class TripLocationViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Trips.objects.all()
    serializer_class = TripLocationSerializer
    filterset_class = TripLocationFilter

    # @property
    # def filter_class(self):
    #     if self.action == "list":
    #         print("filtering ..")
    #         return TripLocationFilter
    
    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        qs = self.queryset
        if self.action == "list":
            if user.is_superuser:
                return self.queryset.order_by("-created_at")
            organization_id = payload["organization_id"]
            qs = self.queryset.filter(vehicle__organization__uuid=organization_id)
            return qs.order_by("-created_at")
        return qs

    # def get_queryset(self):
    #     print("getting data")
    #     return super().get_queryset().order_by('-created_at')


class TripStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trips.objects.all()
    serializer_class = TripStatsSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        organization_id = user.organization_id
        last_7_days = timezone.now() - timedelta(days=7)
        qs = self.queryset.filter(
            created_at__gte=last_7_days,
            vehicle__organization__uuid=organization_id
            ).aggregate(
            total_trips=Count("id"),
            total_distance=Sum("distance"),
            total_duration=Sum("duration"),
            total_incidents=Sum("total_incidents")
            )
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.serializer_class(data=qs)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
