from rest_framework.routers import DefaultRouter
from django.urls import path, include

from alert.apis.viewsets import RealtimeDatabaseViewSet, AlertViewSet
from trip.apis.viewsets import TripViewSet, TripLocationViewSet, TripStatsViewSet

router = DefaultRouter()
router.register("current-location", RealtimeDatabaseViewSet, basename="gps")
router.register("alerts", AlertViewSet, basename="alerts")
router.register("trips", TripViewSet, basename="trips")
router.register("trips-stats", TripStatsViewSet, basename="trips-stats")
router.register("gps-cordinates", TripViewSet, basename="gps-cordinates")

urlpatterns = [
    path("", include(router.urls)),
]
