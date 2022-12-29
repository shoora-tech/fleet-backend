from user.models import Method
from rest_framework.permissions import BasePermission
from organization.models import Organization
from device.models import Device

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


def role_has_access(request, feature, method):
    payload = request.auth.payload
    organization_id = payload["organization_id"]
    roles = payload["roles"]

    if organization_id == None:
        return False
    if organization_has_access_to_feature(organization_id, feature):
        try:
            AccessControl.objects.filter(
                role__uuid__in=roles, method__in=[method.pk], feature=feature
            )
            return True
        except Exception:
            return False
    return False


class AccessControlPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        JWTA = JWTAuthentication()
        user = JWTA.get_user(request.auth.payload)
        print(" view ", view.basename)
        if view.basename == 'device-status':
            return True
        if user.is_superuser:
            return True
        try:
            feature = Feature.objects.get(name=view.basename)
        except Feature.DoesNotExist:
            return False
        try:
            method = Method.objects.get(name=request.method)
        except Method.DoesNotExist:
            return False
        if role_has_access(request, feature, method):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # grant access if the requestor is superuser or of the same organization
        payload = request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        if user.is_superuser:
            return True
        organization_id = payload["organization_id"]
        if view.basename == "organizations":
            if str(obj.uuid) == organization_id:
                return True
        elif view.basename == "alerts":
            print("base is alerts")
            if str(obj.vehicle.organization.uuid) == organization_id:
                return True

        elif view.basename == "gps":
            device = Device.objects.get(imei_number=obj.imei)
            if str(device.organization.uuid) == organization_id:
                return True

        elif view.basename == "trips":
            vehicle = obj.vehicle
            if str(vehicle.organization.uuid) == organization_id:
                return True
        else:
            if str(obj.organization.uuid) == organization_id:
                return True
        return False


class DeviceStatusPermission(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
