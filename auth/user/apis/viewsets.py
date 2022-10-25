from rest_framework import viewsets

from auth.permissions import UserPermission
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        role_objects = user.roles.all().values_list("uuid", flat=True)
        roles = [str(role) for role in role_objects]
        refresh = RefreshToken.for_user(user)
        if user.organization:
            refresh['organization_id'] = str(user.organization.uuid)
        refresh['user_id'] = str(user.uuid)
        refresh['roles'] = roles
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return Response(data, status=status.HTTP_201_CREATED)
