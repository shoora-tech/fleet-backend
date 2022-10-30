from rest_framework.permissions import BasePermission, SAFE_METHODS
import requests
from transport.settings import CHECK_PERMISSION_URL

class VehiclePermission(BasePermission):
    def has_permission(self, request, view):
        data = {
            "feature": "VEHICLE",
            "method": request.method
        }
        headers = {
            "authorization": request.META['HTTP_AUTHORIZATION']
        }
        resp = requests.post(url=CHECK_PERMISSION_URL, headers=headers, data=data)
        print(resp.status_code)
        if resp.status_code != 200:
            return False
        return True
