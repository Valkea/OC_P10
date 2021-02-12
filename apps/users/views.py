# from django.shortcuts import render
#
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
#
# from .models import UserSerializer
#
#
# class CreateUserAPIView(APIView):
#     # Allow any user (authenticated or not) to access this url
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         user = request.data
#         serializer = UserSerializer(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.exceptions import NotFound
from rest_framework import generics

from .models import User
from .serializers import UserSerializer


class UserViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
