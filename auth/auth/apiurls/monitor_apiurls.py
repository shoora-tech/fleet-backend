from rest_framework.routers import DefaultRouter
from django.urls import path, include

from alert.apis.viewsets import RealtimeDatabaseViewSet, AlertViewSet

router = DefaultRouter()
router.register("current-location", RealtimeDatabaseViewSet, basename="gps")
router.register("alerts", AlertViewSet, basename="alerts")

urlpatterns = [
    path("", include(router.urls)),
]
