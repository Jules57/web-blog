from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user making the request is the author of the article
        return obj.author == request.user
