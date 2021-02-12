from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from apps.users.models import User
from apps.users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type"]


class IssueSerializer(serializers.ModelSerializer):

    # author_user = UserSerializer(read_only=True)
    # assignee_user = UserSerializer(read_only=True)
    # project = ProjectSerializer(read_only=True)

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

    # def create(self, validated_data) -> Issue:

    #     print("validated_data:", validated_data)

    #     # key_author_user = User.objects.create(**validated_data.get('author_user'))
    #     # key_assignee_user = User.objects.create(**validated_data.get('assignee_user'))
    #     # key_project = Project.objects.create(**validated_data.get('project'))

    #     # create connection
    #     conn = Issue.objects.create(
    #         title=validated_data.get('title'),
    #         description=validated_data.get('description'),
    #         tag=validated_data.get('tag'),
    #         priority=validated_data.get('priority'),
    #         # project=key_project,
    #         project=validated_data.get('project'),
    #         status=validated_data.get('status'),
    #         # author_user=key_author_user,
    #         author_user=validated_data.get('author_user'),
    #         # assignee_user=key_assignee_user,
    #         assignee_user=validated_data.get('assignee_user'),
    #         created_time=validated_data.get('created_time'),
    #     )
    #     return conn


class CommentSerializer(serializers.ModelSerializer):

    # issue = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ["id", "description", "author_user", "issue", "created_time"]


class ContributorSerializer(serializers.ModelSerializer):

    # user_infos = UserSerializer(source='user', many=False)
    # project_infos = ProjectSerializer(source='project', many=False)

    # user_infos = serializers.ReadOnlyField()
    # project_infos = serializers.ReadOnlyField()

    # user = UserSerializer()
    # project = ProjectSerializer()

    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "user_username", "permission", "role", "project"]
