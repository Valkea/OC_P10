from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    """
    This permission class check whether or not the current user is the
    same as the current User's object that is being manipulated.

    This usually used when updating / deleting user's profiles.
    """

    # called if the view-level
    def has_permission(self, request, view):
        return True

    # called on object level if 'has_permission' is True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj
