# Views for the user API

from rest_framework import generics

from user.serializers import UserSerializer


class createUserView(generics.CreateAPIView):
    # Create new user in system

    serializer_class = UserSerializer
