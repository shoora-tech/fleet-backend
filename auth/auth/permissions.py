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


def role_has_access(request):
    payload = request.auth.payload
    organization_id = payload['organization_id']
    roles = payload['roles']
    action = request.method
    feature = Feature.objects.get(name="USER")
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
        # return True
        JWTA = JWTAuthentication()
        user = JWTA.get_user(request.auth.payload)
        if user.is_superuser:
            return True
        if not request.user.is_authenticated:
            return False
        if role_has_access(request):
            return True
        return False
