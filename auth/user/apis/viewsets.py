from rest_framework import viewsets
from rest_framework import views

from auth.permissions import AccessControlPermission
from .serializers import RoleSerializer, UserSerializer, MyTokenObtainPairSerializer
from user.models import User, Role
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        token = super().post(request, *args, **kwargs)
        JWTA = JWTAuthentication()
        access_token = AccessToken(token.data['access'])
        user = JWTA.get_user(access_token.payload)
        user_serializer = UserSerializer(user, context={'request': request})
        data = user_serializer.data
        data['refresh'] = token.data['refresh']
        data['access'] = token.data['access']
        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        req_data = request.data.copy()
        JWTA = JWTAuthentication()
        user = JWTA.get_user(request.auth.payload)
        if not user.is_superuser:
            req_data.pop('organization_id')
            organization_id = user.organization_id
            req_data['organization_id'] = organization_id
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


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
