from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .serializers import OrganizationSerializer, BranchSerializer
from organization.models import Organization, Branch


class OrganizationViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [AccessControlPermission]

    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        qs = self.queryset
        if self.action == "list" or self.action == "retrieve":
            if user.is_superuser:
                return self.queryset.order_by("-created_at")
            organization_id = payload["organization_id"]
            qs = self.queryset.filter(uuid=organization_id)
            return qs.order_by("-created_at")
        return qs


class BranchViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [AccessControlPermission]

    def get_queryset(self):
        # payload = self.request.auth.payload
        # JWTA = JWTAuthentication()
        user = self.request.user
        qs = self.queryset
        if self.action == "list" or self.action == "retrieve":
            if user.is_superuser:
                return self.queryset.order_by("-created_at")
            # organization_id = user.organization_id
            qs = self.queryset.filter(uuid=user.branch_id)
            return qs.order_by("-created_at")
        return qs
