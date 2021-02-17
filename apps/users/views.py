from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from .models import User
from .serializers import UserSerializer, UserAPISerializer
from .permissions import IsCurrentUser


class UserDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated & IsCurrentUser]
    serializer_class = UserAPISerializer
    queryset = User.objects.all()


class UserSignup(mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserAPISerializer

    def post(self, request, *args, **kwargs):
        print("DEBUG post new user:", request, args, kwargs)
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        serializer = UserAPISerializer(data=request.data)

        if serializer.is_valid():

            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            request.data.update(
                {"password": make_password(request.data.get("password"))}
            )
            if hasattr(request.data, "_mutable"):
                request.data._mutable = False
            serializer = UserAPISerializer(data=request.data)

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
