from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAccessControlAuthentication(authentication.BaseAuthentication):
    # def role_has_access(role, action, feature):

    def authenticate(self, request):
        print("request is ", request)
        print("claims ", token.payload)
        User = get_user_model()
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user, token = response
            return (user, None)
            # check if user has permission
            # print("this is decoded token claims", token.payload)
        else:
            print("no token is provided in the header or the header is missing")

        return None
