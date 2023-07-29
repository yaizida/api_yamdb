from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not user.is_anonymous and user.is_admin
