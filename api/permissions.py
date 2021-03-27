from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated)
            and (
                (request.user.is_staff)
                or (request.user.is_superuser)
                or (request.user.role == 'admin')
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (
            (request.user.is_staff)
            or (request.user.is_superuser)
            or (request.user.role == 'admin')
            or (request.method in permissions.SAFE_METHODS)
        )


class IsOwnerOrModerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (
            (request.user.is_staff)
            or (request.user.is_superuser)
            or (obj.author == request.user)
            or (request.user.role == 'admin')
            or (request.user.role == 'moderator')
            or (request.method in permissions.SAFE_METHODS)
        )
