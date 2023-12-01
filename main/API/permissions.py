from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.author == request.user

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.author == request.user

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.pk
