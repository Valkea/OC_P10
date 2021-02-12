from rest_framework import serializers
from .models import User
from apps.api_issue_tracking.models import Contributor


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()
    # contributor = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())

    class Meta(object):
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "date_joined", "last_login", "password", "is_active", "is_staff", "is_superuser")
        extra_kwargs = {"password": {"write_only": True}}
