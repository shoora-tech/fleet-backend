from rest_framework.routers import DefaultRouter
from django.urls import path, include

from organization.apis.viewsets import OrganizationViewSet
from user.apis.viewsets import UserViewSet, MyTokenObtainPairView, RoleViewSet
from feature.apis.viewsets import FeatureViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from vehicle.apis.viewsets import VehicleViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('features', FeatureViewSet, basename='features')
router.register('roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", include(router.urls)),
]
