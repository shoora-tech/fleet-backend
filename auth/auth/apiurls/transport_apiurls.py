from rest_framework.routers import DefaultRouter
from django.urls import path, include

from vehicle.apis.viewsets import VehicleViewSet
from driver.apis.viewsets import DriverViewSet
from device.apis.viewsets import DeviceViewSet
from alert.apis.viewsets import RealtimeDatabaseViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicles")
router.register("drivers", DriverViewSet, basename="drivers")
router.register("devices", DeviceViewSet, basename="devices")
router.register("gps", RealtimeDatabaseViewSet, basename="alerts")

urlpatterns = [
    path("", include(router.urls)),
]
