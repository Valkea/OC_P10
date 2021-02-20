from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from .models import User
from .serializers import UserFullSerializer, UserMiniSerializer
from .permissions import IsCurrentUser


class UserDetailsViewSet(viewsets.ModelViewSet):
    """
    Display :model:`users.User` instances using the UserFullSerializer

    These are the FULL user views
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFullSerializer
    queryset = User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    """
    Display :model:`users.User` instances using the UserMiniSerializer

    These are the LIGHT user views
    """

    permission_classes = [permissions.IsAuthenticated & IsCurrentUser]
    serializer_class = UserMiniSerializer
    queryset = User.objects.all()


class UserSignup(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Display :model:`users.User` instances using the UserMiniSerializer

    This is a LIGHT user view just like UserViewSet, but they are
    separated because the permissions are differents.
    """

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserMiniSerializer

    def post(self, request, *args, **kwargs):
        """ Allows to POST data to the API in order to create a new user """
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Custom create method used to encrypt password before inserting data in the DB """

        serializer = UserMiniSerializer(data=request.data)

        if serializer.is_valid():

            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            request.data.update(
                {"password": make_password(request.data.get("password"))}
            )
            if hasattr(request.data, "_mutable"):
                request.data._mutable = False
            serializer = UserMiniSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

            content = {
                key: value
                for key, value in request.data.items()
                if key not in ["csrfmiddlewaretoken", "password"]
            }
            content["id"] = User.objects.get(username=content["username"]).id

            return Response(content, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
