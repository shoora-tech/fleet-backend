from rest_framework.routers import DefaultRouter
from django.urls import path, include

from alert.apis.viewsets import RealtimeDatabaseViewSet

router = DefaultRouter()
router.register("current-location", RealtimeDatabaseViewSet, basename="gps")

urlpatterns = [
    path("", include(router.urls)),
]
