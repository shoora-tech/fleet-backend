from rest_framework.permissions import BasePermission, SAFE_METHODS
from organization.models import Organization

from user.models import AccessControl
from feature.models import Feature
from rest_framework_simplejwt.authentication import JWTAuthentication


def organization_has_access_to_feature(organization_id, feature):
    try:
        organization = Organization.objects.get(uuid=organization_id)
        try:
            feature = organization.features.all().filter(name=feature.name)
            if feature:
                return True
            return False
        except Feature.DoesNotExist:
            return False
    except Organization.DoesNotExist:
        return False


def role_has_access(request, feature, action):
    payload = request.auth.payload
    organization_id = payload['organization_id']
    roles = payload['roles']
    
    
    if organization_id == None:
        return False
    if organization_has_access_to_feature(organization_id, feature):
        try:
            AccessControl.objects.get(role__uuid__in=roles, action=action, feature=feature)
            return True
        except AccessControl.DoesNotExist:
            return False
    return False

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        JWTA = JWTAuthentication()
        user = JWTA.get_user(request.auth.payload)
        if user.is_superuser:
            return True
        action = request.method
        feature = Feature.objects.get(name="USER")
        if role_has_access(request, feature, action):
            return True
        return False


class ExternalPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        JWTA = JWTAuthentication()
        user = JWTA.get_user(request.auth.payload)
        if user.is_superuser:
            return True
        data = request.data

        feature = feature = Feature.objects.get(name=data.get('feature'))
        action = data.get('method')
        if role_has_access(request, feature, action):
            return True
        return False


