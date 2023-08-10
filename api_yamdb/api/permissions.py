from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """AdminOnly permission.
    Разрешает доступ к ресурсу, если пользователь аутентифицирован и является
    администратором или суперпользователем.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Класс для проверки прав доступа к API."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
