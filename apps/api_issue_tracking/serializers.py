from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type"]

    def create(self, validated_data):

        print("create:", validated_data)

        new_project = Project.objects.create(**validated_data)

        Contributor.objects.create(
            user=self.context["request"].user,
            permission=Contributor.Permission.ALL,
            role=Contributor.Role.OWNER,
            project=new_project,
        )

        return new_project


class IssueSerializer(serializers.ModelSerializer):

    author_username = serializers.CharField(
        source="author_user.username", read_only=True
    )
    assignee_username = serializers.CharField(
        source="assignee_user.username", read_only=True
    )

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
            "author_username",
            "assignee_user",
            "assignee_username",
            "created_time",
        ]


class CommentSerializer(serializers.ModelSerializer):

    author_username = serializers.CharField(
        source="author_user.username", read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "description",
            "author_user",
            "author_username",
            "issue",
            "created_time",
        ]


class ContributorSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "user_username", "permission", "role", "project"]
