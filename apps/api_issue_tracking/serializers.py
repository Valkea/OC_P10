from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from apps.users.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type"]


class IssueSerializer(serializers.ModelSerializer):

    # author_user_id = serializers.ReadOnlyField()
    # created_time = serializers.ReadOnlyField()
    # project_id = serializers.RelatedField(source='project', read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "project_id",
            "status",
            "author_user_id",
            "assignee_user_id",
            "created_time",
        ]


class CommentSerializer(serializers.ModelSerializer):

    # issue = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ["id", "description", "author_user_id", "issue_id", "created_time"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ContributorSerializer(serializers.ModelSerializer):

    # user_infos = UserSerializer(source='user', many=False)
    # project_infos = ProjectSerializer(source='project', many=False)

    # user_infos = serializers.ReadOnlyField()
    # project_infos = serializers.ReadOnlyField()

    # user = UserSerializer()
    # project = ProjectSerializer()

    # user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        # fields = ["id", "user_id", "user_username", "permission", "role", "project_id"]
        fields = ["id", "user_id", "permission", "role", "project_id"]
