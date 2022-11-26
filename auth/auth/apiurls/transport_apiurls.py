from rest_framework.routers import DefaultRouter
from django.urls import path, include

from vehicle.apis.viewsets import VehicleViewSet,VehicleMakeViewSet,VehicleTypeViewSet,VehicleModelViewSet
from driver.apis.viewsets import DriverViewSet
from device.apis.viewsets import DeviceViewSet
from alert.apis.viewsets import AlertViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicles")
router.register("vehicle-makes", VehicleMakeViewSet, basename="vehiclemakes")
router.register("vehicle-models", VehicleModelViewSet, basename="vehiclemodels")
router.register("vehicle-types", VehicleTypeViewSet, basename="vehicletypes")
router.register("drivers", DriverViewSet, basename="drivers")
router.register("devices", DeviceViewSet, basename="devices")
router.register("alerts", AlertViewSet, basename="alerts")

urlpatterns = [
    path("", include(router.urls)),
]
