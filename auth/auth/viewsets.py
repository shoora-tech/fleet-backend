from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


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

    def create(self, request, *args, **kwargs):
        req_data = request.data.copy()
        payload = self.request.auth.payload
        organization_id = payload["organization_id"]
        req_data["organization_id"] = organization_id
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
