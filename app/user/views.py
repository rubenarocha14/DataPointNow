# Views for the user API

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import UserSerializer, AuthTokenSerializer


class createUserView(generics.CreateAPIView):
    # Create new user in system

    serializer_class = UserSerializer


class createTokenView(ObtainAuthToken):
    # Create new auth token fro user

    serializer_class = AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES


class manageUserView(generics.RetrieveUpdateAPIView):
    # Manage the auth user
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get and return auth user
        return self.request.user
