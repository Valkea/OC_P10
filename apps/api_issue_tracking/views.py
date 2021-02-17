# from django.shortcuts import render
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
from .permissions import IsOwnerOrContributor, IsProjectOwer, IsProjectContributor, IsProjectList

# from rest_framework import mixins
# from rest_framework import generics

# class ProjectList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ProjectDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class ProjectViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer)
        | (permissions.IsAuthenticated & IsProjectContributor)
        | (permissions.IsAuthenticated & IsProjectList)
    ]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):  # TODO Can I remove it ?
        print("CREATE PROJECT VIEWSET:", self, request, args, kwargs)
        return super().create(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     print("UPDATE PROJECT VIEWSET:", self, request, args, kwargs)
    #     content = super().update(request, *args, **kwargs)
    #     # return Response(content, status=status.HTTP_201_CREATED)
    #     #return HttpResponse(content, content_type="application/json", status=status.HTTP_201_CREATED)
    #     # return HttpResponse(status=201)

    # def save(self, request, *args, **kwargs):
    #     print("SAVE PROJECT VIEWSET:", self, request, args, kwargs)


class IssueViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated & IsContributor]
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrContributor]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            return self.queryset.filter(project=project)

        except Project.DoesNotExist:
            raise NotFound(f"Project (id:{project_id}) does not exist")

    # def update(self, request, *args, **kwargs):
    #     try:
    #         project_id = self.kwargs.get("project_pk")
    #         Project.objects.get(id=project_id)

    #         issue_id = self.kwargs.get("pk")
    #         issue = Issue.objects.get(id=issue_id)

    #         serializer = self.serializer_class(issue, data=request.data)

    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     except Project.DoesNotExist:
    #         raise NotFound(f"A Project with id {project_id} does not exist")
    #     except Issue.DoesNotExist:
    #         raise NotFound(f"An Issue with id {issue_id} does not exist")

    def create(self, request, *args, **kwargs):
        print("CREATE ISSUE VIEWSET:", self, request, args, kwargs)

        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            request.data.update({"author_user": request.user.id})
            request.data.update({"project": project.id})

            return super().create(request, *args, **kwargs)

            # serializer = self.serializer_class(Issue(), data=request.data)

            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            raise NotFound(f"Project (id:{project_id}) does not exist")


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrContributor]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self, *args, **kwargs):

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
        print("CREATE COMMENT VIEWSET:", self, request, args, kwargs)

        try:
            issue_id = self.kwargs.get("issue_pk")
            issue = Issue.objects.get(id=issue_id)

            print("REQUEST USER NEW COMMENT:", request.user)

            request.data.update({"author_user": request.user.id})
            request.data.update({"issue": issue.id})

            return super().create(request, *args, **kwargs)

            serializer = self.serializer_class(Comment(), data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Issue.DoesNotExist:
            raise NotFound(f"Issue (id: {issue_id}) does not exist")


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = [
        (permissions.IsAuthenticated & IsProjectOwer) |
        (permissions.IsAuthenticated & IsProjectContributor)
    ]
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_queryset(self, *args, **kwargs):

        try:
            project_id = self.kwargs.get("project_pk")
            project = Project.objects.get(id=project_id)

            return self.queryset.filter(project=project)

        except Project.DoesNotExist:
            raise NotFound(f"A Project with id {project_id} does not exist")
