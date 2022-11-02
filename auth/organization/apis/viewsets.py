from auth.permissions import AccessControlPermission
from rest_framework import viewsets
from .serializers import OrganizationSerializer
from organization.models import Organization


class OrganizationViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [AccessControlPermission]
