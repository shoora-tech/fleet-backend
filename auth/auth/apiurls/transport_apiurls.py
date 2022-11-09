from rest_framework.routers import DefaultRouter
from django.urls import path, include

from vehicle.apis.viewsets import VehicleViewSet
from driver.apis.viewsets import DriverViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicles")
router.register("drivers", DriverViewSet, basename="drivers")

urlpatterns = [
    path("", include(router.urls)),
]
