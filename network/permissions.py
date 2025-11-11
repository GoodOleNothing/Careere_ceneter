from rest_framework import permissions


class IsActiveStaffEmployee(permissions.BasePermission):
    """
    Доступ только для активных сотрудников
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
