from rest_framework import serializers

from .models import Project, Issue, Comment, Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """ This serializer returns a translation of the Contributor model. """

    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "user_username", "permission", "role", "project"]


class ProjectSerializer(serializers.ModelSerializer):
    """
    This serializer returns a translation of the Project model,
    extended with lists of the current projet's ADMINISTRATORS and CONTRIBUTORS.
    """

    administrators = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "administrators",
            "contributors",
        ]

    def create(self, validated_data):
        """ Make sure to add the project creator as its first contributor """

        new_project = Project.objects.create(**validated_data)

        Contributor.objects.create(
            user=self.context["request"].user,
            permission=Contributor.Permission.ALL,
            role=Contributor.Role.ADMINISTRATOR,
            project=new_project,
        )

        return new_project

    def get_administrators(self, obj):
        """ Extend the current serializer to list the current project ADMINISTRATORS """
        selected = Contributor.objects.filter(
            project=obj, role=Contributor.Role.ADMINISTRATOR
        )  # .distinct()

        return ContributorSerializer(selected, many=True).data

    def get_contributors(self, obj):
        """ Extend the current serializer to list the current project CONTRIBUTORS """
        selected = Contributor.objects.filter(
            project=obj, role=Contributor.Role.CONTRIBUTOR
        )  # .distinct()

        return ContributorSerializer(selected, many=True).data


class IssueSerializer(serializers.ModelSerializer):
    """
    This serializer returns a translation of the Issue model,
    extended with the author_user and assignee_user usernames
    in order to improve readibility (not really usefull for
    a real API)
    """

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
    """
    This serializer returns a translation of the Comment model,
    extended with the author_user username in order to improve
    readibility (not really usefull for a real API)
    """

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
