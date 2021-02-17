from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):

    # called if the view-level
    def has_permission(self, request, view):
        return True

    # called on object level if 'has_permission' is True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj
