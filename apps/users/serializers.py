from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User
from apps.api_issue_tracking.models import Comment, Issue


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer returns a translation of the FULL User model
    extended with the user's created & assigned issues.

    It is used whenever we need a very complete user's profile.
    """

    date_joined = serializers.ReadOnlyField()
    comments_id = serializers.PrimaryKeyRelatedField(
        source="comment_author", many=True, queryset=Comment.objects.all()
    )

    issues_id = serializers.PrimaryKeyRelatedField(
        source="author_user", many=True, queryset=Issue.objects.all()
    )

    assignments_id = serializers.PrimaryKeyRelatedField(
        source="assignee_user", many=True, queryset=Issue.objects.all()
    )

    # contributor_user = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Contributor.objects.all()
    # )

    class Meta(object):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "comments_id",
            "issues_id",
            "assignments_id",
            # "contributor_user",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserAPISerializer(serializers.ModelSerializer):
    """
    This serializer returns a LIGHT translation of the User model
    extended with the user's created & assigned issues.

    It is used whenever we need the bare minumum user's information.
    """

    class Meta(object):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        # extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        """ Make sure to encode the password when updating the user's profile """

        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.password = make_password(
            validated_data.get("password", instance.password)
        )
        instance.save()
        return instance
