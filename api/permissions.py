from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


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


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return (
#             (obj.author == request.user)
#             or (request.method in permissions.SAFE_METHODS)
#             or request.user.is_staff
#         )


# class IsOwnerOnly(permissions.BasePermission):
#     def has_permission(self, request, view, obj):
#         return obj.author == request.user

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user and
                request.user.is_authenticated and
                obj.author == request.user)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated and
                request.user.is_active and
                request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.user and
                request.user.is_active and
                request.user.is_authenticated and
                request.user.is_admin)


class IsModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user and
                request.user.is_active and
                request.user.is_authenticated and
                request.user.is_moderator)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
