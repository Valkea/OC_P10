# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework import permissions

from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
)
from .permissions import IsOwnerOrContributor, IsProjectOwer, IsProjectContributor


class ProjectViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer) | (permissions.IsAuthenticated & IsProjectContributor)
            ]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class IssueViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated & IsContributor]
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrContributor]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
        return self.queryset.filter(project=project)

    # def perform_create(self, serializer):
    #     print("serializer:", serializer)
    #     print("========>", serializer.validated_data['author_user'], "<===========")
    #     if serializer.validated_data['author_user']:
    #         serializer.save()
    #     else:
    #         serializer.save(author_user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated & IsContributor]
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrContributor]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        issue_id = self.kwargs.get("issue_pk")
        try:
            Project.objects.get(id=project_id)

            try:
                issue = Issue.objects.get(id=issue_id, project=project_id)
            except Issue.DoesNotExist:
                raise NotFound(
                    f"An Issue with id {issue_id} does not exist in Project {project_id}"
                )

        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
        return self.queryset.filter(issue=issue)


class ContributorViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrContributor]
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
        return self.queryset.filter(project=project)
