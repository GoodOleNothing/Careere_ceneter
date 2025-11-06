from rest_framework import permissions


class IsActiveStaffEmployee(permissions.BasePermission):
    """
    Доступ к API только для активных сотрудников (залогиненных пользователей),
    у которых is_active=True и is_staff=True.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
