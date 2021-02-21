from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
)
from .permissions import IsProjectOwer, IsProjectContributor, IsProjectList


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Display :model:`api_issue_tracking.Project` instances using the ProjectSerializer
    """

    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer)
        | (permissions.IsAuthenticated & IsProjectContributor)
        | (permissions.IsAuthenticated & IsProjectList)
    ]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class IssueViewSet(viewsets.ModelViewSet):
    """
    Display :model:`api_issue_tracking.Issue` instances using the IssueSerializer
    """

    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer)
        | (permissions.IsAuthenticated & IsProjectContributor)
    ]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    def get_queryset(self, *args, **kwargs):
        """ Handle nested project's 'pk' in the URI """
        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            return self.queryset.filter(project=project)

        except Project.DoesNotExist:
            raise NotFound(f"Project (id:{project_id}) does not exist")

    def create(self, request, *args, **kwargs):
        """ Custom create method used to setup the issue's Foreign-keys (author_user & project) """

        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            request.data.update({"author_user": request.user.id})
            request.data.update({"project": project.id})

            return super().create(request, *args, **kwargs)

        except Project.DoesNotExist:
            raise NotFound(f"Project (id:{project_id}) does not exist")

    def update(self, request, *args, **kwargs):
        """ Custom update method used to protect the issue's Foreign-keys (author_user & project) """
        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            request.data.update({"author_user": request.user.id})
            request.data.update({"project": project.id})

            return super().update(request, *args, **kwargs)

        except Project.DoesNotExist:
            raise NotFound(f"Project (id:{project_id}) does not exist")


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer)
        | (permissions.IsAuthenticated & IsProjectContributor)
    ]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self, *args, **kwargs):
        """ Handle nested project's and issue's 'pk' in the URI """
        try:
            project_id = self.kwargs.get("project_pk")
            Project.objects.get(id=project_id)

            issue_id = self.kwargs.get("issue_pk")
            issue = Issue.objects.get(id=issue_id, project=project_id)

            return self.queryset.filter(issue=issue)

        except Project.DoesNotExist:
            raise NotFound(f"Project (id:{project_id}) does not exist")
        except Issue.DoesNotExist:
            raise NotFound(
                f"Issue (id:{issue_id}) does not exist in Project (id:{project_id})"
            )

    def create(self, request, *args, **kwargs):
        """ Custom create method used to setup the comment's Foreign-keys (author_user & issue) """

        try:
            issue_id = self.kwargs.get("issue_pk")
            issue = Issue.objects.get(id=issue_id)

            request.data.update({"author_user": request.user.id})
            request.data.update({"issue": issue.id})

            return super().create(request, *args, **kwargs)

        except Issue.DoesNotExist:
            raise NotFound(f"Issue (id: {issue_id}) does not exist")

    def update(self, request, *args, **kwargs):
        """ Custom update method used to protect the comment's Foreign-keys (author_user & issue) """

        try:
            issue_id = self.kwargs.get("issue_pk")
            issue = Issue.objects.get(id=issue_id)

            request.data.update({"author_user": request.user.id})
            request.data.update({"issue": issue.id})

            return super().update(request, *args, **kwargs)

        except Issue.DoesNotExist:
            raise NotFound(f"Issue (id: {issue_id}) does not exist")


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer)
        | (permissions.IsAuthenticated & IsProjectContributor)
    ]
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_queryset(self, *args, **kwargs):
        """ Handle nested project's 'pk' in the URI """

        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            return self.queryset.filter(project=project)

        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
