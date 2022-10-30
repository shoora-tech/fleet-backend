from django.db import router
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from vehicle.apis.viewsets import VehicleViewSet

router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='vehicles')

urlpatterns = [
    path("", include(router.urls)),
]
