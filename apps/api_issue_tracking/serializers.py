from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type"]

    def create(self, validated_data):

        print("CREATE PROJECT SERIALIZER:", self, validated_data)

        new_project = Project.objects.create(**validated_data)

        Contributor.objects.create(
            user=self.context["request"].user,
            permission=Contributor.Permission.ALL,
            role=Contributor.Role.OWNER,
            project=new_project,
        )

        return new_project

    # def update(self, instance, validated_data):
    #     print("UPDATE PROJECT SERIALIZER:", self, validated_data)
    #     super().update(instance, validated_data)
    #     return instance

    # def save(self, validated_data):
    #     return validated_data


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

    # def create(self, validated_data):

    #     print("CREATE ISSUE SERIALIZER:", self, validated_data)
    #     return Issue.objects.create(**validated_data)


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
