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
