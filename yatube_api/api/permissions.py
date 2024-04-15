from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndAuthorOrReadOnly(BasePermission):
    """Allows access only to authenticated users, and further restricts
    the ability to edit to the author of the object."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Custom permission to only allow admins to create an object."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)
