from rest_framework import permissions

from .models import Project, Issue, Comment, Contributor


def has_contrib_permission(contrib, request):
    if contrib.permission == Contributor.Permission.NONE:
        print("HASC 01 False")
        return False
    elif contrib.permission == Contributor.Permission.READONLY:
        print("HASC 02", request.method in permissions.SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS
    print("HASC 03 True")
    return True


class IsProjectOwer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("IsProjectOwer OBJ :", request, view, obj)

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
    def has_object_permission(self, request, view, obj):
        print("IsProjectContributor:", request, view, obj)

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
    def has_permission(self, request, view):

        try:
            contrib = Contributor.objects.get(
                user=request.user, project=view.kwargs.get("project_pk")
            )
            return has_contrib_permission(contrib, request)

        except Contributor.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author_user == request.user


# class IsContributor(permissions.BasePermission):
#     """
#     Custom permission verying that the current user is a contributor
#     of the current project / issue / comment
#     """
#     def has_permission(self, request, view):
#
#         """ Give permissions to SAFE_METHODS if the user is one of the contributor of the project.
#             Also check the Contributor permission attribute as an extra permission layer.
#         """
#
#         try:
#             if "project_pk" in view.kwargs:
#                 contrib = Contributor.objects.get(user=request.user, project=view.kwargs.get("project_pk"))
#             elif "pk" in view.kwargs:
#                 contrib = Contributor.objects.get(user=request.user, project=view.kwargs.get("pk"))
#             else:
#                 return True
#
#             if contrib.permission == Contributor.Permission.NONE:
#                 return False
#             elif contrib.permission == Contributor.Permission.READONLY:
#                 return request.method in permissions.SAFE_METHODS
#
#             return True
#
#         except Contributor.DoesNotExist:
#             return False
#
#     def has_object_permission(self, request, view, obj):
#
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         if(type(obj) == Project):
#             print("IsContributor Project:", request.user, obj)
#             try:
#                 contrib = Contributor.objects.get(user=request.user, project=obj)
#                 if contrib.role == Contributor.Role.OWNER:
#                     return True
#                 return False
#             except Contributor.DoesNotExist:
#                 return False
#
#             return Contributor.objects.filter(user=request.user, project=obj).exists()
#
#         elif(type(obj) == Issue):
#             print("IsContributor Issue:", obj.author_user, request.user)
#             return obj.author_user == request.user
#
#         elif(type(obj) == Comment):
#             print("IsContributor Comment:", obj.author_user, request.user)
#             return obj.author_user == request.user
#
#         return False
