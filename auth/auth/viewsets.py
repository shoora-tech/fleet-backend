from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        payload = self.request.auth.payload
        JWTA = JWTAuthentication()
        user = JWTA.get_user(payload)
        qs = self.queryset
        if self.action == "list":
            if user.is_superuser:
                return self.queryset.order_by("-created_at")
            organization_id = payload["organization_id"]
            qs = self.queryset.filter(organization__uuid=organization_id)
            return qs.order_by("-created_at")
        return qs
