from rest_framework import permissions

from .models import Project, Contributor  # , Issue, Comment


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


class IsProjectOwer(permissions.BasePermission):

    # called if the view-level
    def has_permission(self, request, view):
        print(">>>>> IsProjectOwer > has_permission :", request, view)
        return True

    # called on object level if 'has_permission' is True
    def has_object_permission(self, request, view, obj):
        print(">>>>> IsProjectOwer > has_object_permission :", request, view, obj)

        if type(obj) == Project:
            current_project = obj
        elif type(obj) == Contributor:
            current_project = obj.project
        else:
            return False

        try:
            contrib = Contributor.objects.get(
                user=request.user, project=current_project, role=Contributor.Role.OWNER
            )

            return has_contrib_permission(contrib, request)

        except Contributor.DoesNotExist:
            return False


class IsProjectContributor(permissions.BasePermission):

    # called if the view-level
    def has_permission(self, request, view):
        print(">>>>> IsProjectContributor > has_permission :", request, view)
        return True

    # called on object level if 'has_permission' is True
    def has_object_permission(self, request, view, obj):
        print(
            ">>>>> IsProjectContributor > has_object_permission :", request, view, obj
        )

        if type(obj) == Project:
            current_project = obj
        elif type(obj) == Contributor:
            current_project = obj.project
        else:
            return False

        try:
            contrib = Contributor.objects.get(
                user=request.user,
                project=current_project,
                role=Contributor.Role.CONTRIBUTOR,
            )

            if has_contrib_permission(contrib, request):
                return request.method in permissions.SAFE_METHODS
            return False

        except Contributor.DoesNotExist:
            return False


class IsOwnerOrContributor(permissions.BasePermission):

    # called if the view-level
    def has_permission(self, request, view):
        print(">>>>> IsOwnerOrContributor > has_permission :", request, view)

        try:
            contrib = Contributor.objects.get(
                user=request.user, project=view.kwargs.get("project_pk")
            )
            return has_contrib_permission(contrib, request)

        except Contributor.DoesNotExist:
            return False

    # called on object level if 'has_permission' is True
    def has_object_permission(self, request, view, obj):
        print(">>>>> IsOwnerOrContributor > has_object_permission :", request, view)

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author_user == request.user
