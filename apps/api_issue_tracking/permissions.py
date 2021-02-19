from rest_framework import permissions
from django.urls import resolve


from .models import Project, Contributor, Issue, Comment


def has_contrib_permission(contrib, request):
    if contrib.permission == Contributor.Permission.NONE:
        return False
    elif contrib.permission == Contributor.Permission.READONLY:
        return request.method in permissions.SAFE_METHODS
    return True


class IsProjectList(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Return True is the current view the the project listing """

        if request.path == "/projects/":
            return True
        return False


class IsProjectOwer(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Define the Project's admins permissions on views """

        # Is the current user really an admin of this project ?
        try:
            project_id = view.kwargs.get("project_pk")
            if project_id is None:
                project_id = view.kwargs.get("pk")

            contrib = Contributor.objects.get(
                user=request.user, project=project_id, role=Contributor.Role.OWNER
            )
            return has_contrib_permission(contrib, request)

        except Contributor.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """ Define the Project's admins permissions on object level """

        if type(obj) == Issue:
            return request.user == obj.author_user
        elif type(obj) == Comment:
            return request.user == obj.author_user

        return True


class IsProjectContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Define the Project's contributors permissions on views """

        # Is an URI that can't be edited/deleted/created by contributors ?
        current_url = resolve(request.path_info).url_name
        if current_url in ["project", "project_users", "project_user"]:
            if request.method not in permissions.SAFE_METHODS:
                return False

        # Is the current user really a contributor of this project ?
        try:
            project_id = view.kwargs.get("project_pk")
            if project_id is None:
                project_id = view.kwargs.get("pk")

            contrib = Contributor.objects.get(
                user=request.user, project=project_id, role=Contributor.Role.CONTRIBUTOR
            )
            return has_contrib_permission(contrib, request)

        except Contributor.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """ Define the Project's contributors permissions on object level """

        if type(obj) == Issue:
            return request.user == obj.author_user
        elif type(obj) == Comment:
            return request.user == obj.author_user
        elif type(obj) == Project:
            return False
        elif type(obj) == Contributor:
            return False

        return True
