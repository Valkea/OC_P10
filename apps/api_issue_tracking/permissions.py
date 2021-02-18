from rest_framework import permissions
from django.urls import resolve


from .models import Project, Contributor, Issue, Comment


def has_contrib_permission(contrib, request):
    print(">>>>> has_contrib_permission :", request, contrib)
    if contrib.permission == Contributor.Permission.NONE:
        print(">>>>>>> has_contrib_permission 01 False")
        return False
    elif contrib.permission == Contributor.Permission.READONLY:
        print(
            ">>>>>>> has_contrib_permission 02",
            request.method in permissions.SAFE_METHODS,
        )
        return request.method in permissions.SAFE_METHODS
    print(">>>>>>> has_contrib_permission 03 True")
    return True


class IsProjectList(permissions.BasePermission):
    def has_permission(self, request, view):
        print(">>>>> IsProjectList > has_permission :", request, view, request.path)
        if request.path == "/projects/":
            return True
        return False


class IsProjectOwer(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Define the Project's admins permissions on views """

        print(">>>>> IsProjectOwer > has_permission :", request, view)
        print(
            "debug:", request.user, view.kwargs.get("project_pk"), view.kwargs.get("pk")
        )

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

        print(">>>>> IsProjectOwer > has_object_permission :", request, view, obj)

        if type(obj) == Issue:
            return request.user == obj.author_user
        elif type(obj) == Comment:
            return request.user == obj.author_user

        return True


class IsProjectContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Define the Project's contributors permissions on views """

        print(">>>>> IsProjectContributor > has_permission :", request, view)
        print(
            "debug:", request.user, view.kwargs.get("project_pk"), view.kwargs.get("pk")
        )

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

        print(
            ">>>>> IsProjectContributor > has_object_permission :", request, view, obj
        )

        if type(obj) == Issue:
            return request.user == obj.author_user
        elif type(obj) == Comment:
            return request.user == obj.author_user
        elif type(obj) == Project:
            return False
        elif type(obj) == Contributor:
            return False

        return True
