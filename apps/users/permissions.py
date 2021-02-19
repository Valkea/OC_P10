from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    """Give permission if the current user is the same as the User's object,
    so he/she can modify its information.
    """

    # called if the view-level
    def has_permission(self, request, view):
        return True

    # called on object level if 'has_permission' is True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj
