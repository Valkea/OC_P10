from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "project",
            "status",
            "author_user",
            "assignee_user",
            "created_time",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author_user", "issue", "created_time"]


class ContributorSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "user_username", "permission", "role", "project"]
