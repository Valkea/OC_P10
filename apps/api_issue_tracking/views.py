from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    # queryset = Issue.objects.all()

    queryset = Issue.objects.all().select_related("project")
    # ).prefetch_related(
    #    'authors'
    # )

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
        return self.queryset.filter(project=project)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # queryset = Comment.objects.all()

    queryset = Comment.objects.all().select_related("issue")
    # ).prefetch_related(
    #    'authors'
    # )

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
    serializer_class = ContributorSerializer
    # queryset = Contributor.objects.all()

    queryset = Contributor.objects.all()
    # .select_related("project")
    # .prefetch_related("authors")
    print("ContributorViewSet:", queryset)

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
        return self.queryset.filter(project=project)
