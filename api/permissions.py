from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated)
            and ((request.user.is_staff)
            or (request.user.is_superuser)
            or (request.user.role == 'admin'))
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
