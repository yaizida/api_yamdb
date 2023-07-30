"""Модуль с классами для проверки прав доступа к API."""
from rest_framework import permissions


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Класс для проверки прав доступа к API."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user == obj.author or
            request.user.is_staff or
            request.user.is_moderator or
            request.user.is_admin
        )
