from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return all([
            (request.user.is_authenticated)
            and any([
                request.user.is_staff,
                request.user.is_superuser,
                request.user.is_admin
            ])
        ])


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return any([
            request.user.is_staff,
            request.user.is_superuser,
            request.user.is_admin,
            request.method in permissions.SAFE_METHODS
        ])


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return all([
            request.user,
            request.user.is_authenticated,
            obj.author == request.user
        ])



class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return all([
            request.user,
            request.user.is_authenticated,
            request.user.is_active,
            request.user.is_admin
        ])


    def has_object_permission(self, request, view, obj):
        return all([
            request.user,
            request.user.is_active,
            request.user.is_authenticated,
            request.user.is_admin
        ])


class IsModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return all([
            request.user,
            request.user.is_active,
            request.user.is_authenticated,
            request.user.is_moderator
        ])


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
